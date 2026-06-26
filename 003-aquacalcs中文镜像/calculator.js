(function() {
    "use strict";

    // ---- Utility formatters ----
    var fmt = {
        currency: function(v, decimals) {
            decimals = decimals !== undefined ? decimals : 2;
            var sign = v < 0 ? "-" : "";
            var abs = Math.abs(v);
            var parts = abs.toFixed(decimals).split(".");
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            return sign + "$" + parts.join(".");
        },
        percentage: function(v, decimals) {
            decimals = decimals !== undefined ? decimals : 2;
            return v.toFixed(decimals) + "%";
        },
        number: function(v, decimals) {
            decimals = decimals !== undefined ? decimals : 2;
            var parts = v.toFixed(decimals).split(".");
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            return parts.join(".");
        },
        integer: function(v) {
            return Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    };

    // ---- Read form inputs ----
    function readInputs(formEl) {
        var inputs = {};
        var fields = formEl.querySelectorAll("input, select");
        for (var i = 0; i < fields.length; i++) {
            var f = fields[i];
            var name = f.getAttribute("name");
            if (!name) continue;
            if (f.type === "checkbox") {
                inputs[name] = f.checked;
            } else if (f.tagName === "SELECT") {
                inputs[name] = f.value;
            } else {
                var raw = f.value.replace(/[^\d.\-]/g, "");
                inputs[name] = raw === "" ? 0 : parseFloat(raw);
            }
        }
        return inputs;
    }

    // ---- Validate inputs ----
    function validate(inputs, rules) {
        if (!rules) return null;
        for (var i = 0; i < rules.length; i++) {
            var r = rules[i];
            var val = inputs[r.field];
            if (r.required && (val === undefined || val === "" || val === 0)) {
                return r.message || (r.field + " is required.");
            }
            if (r.min !== undefined && val < r.min) {
                return r.message || (r.field + " must be at least " + r.min + ".");
            }
            if (r.max !== undefined && val > r.max) {
                return r.message || (r.field + " must be at most " + r.max + ".");
            }
        }
        return null;
    }

    // ---- Display results ----
    function displayResults(results, container) {
        container.innerHTML = "";
        if (!results || !results.length) return;

        for (var i = 0; i < results.length; i++) {
            var r = results[i];
            var row = document.createElement("div");
            row.className = "result-row";

            var label = document.createElement("span");
            label.className = "result-label";
            label.textContent = r.label;

            var value = document.createElement("span");
            value.className = "result-value";

            var formatted;
            var rawVal = r.value;
            switch (r.format) {
                case "currency": formatted = fmt.currency(rawVal, r.decimals); break;
                case "percentage": formatted = fmt.percentage(rawVal, r.decimals); break;
                case "integer": formatted = fmt.integer(rawVal); break;
                case "text": formatted = String(rawVal); break;
                default: formatted = fmt.number(rawVal, r.decimals);
            }
            value.textContent = formatted;

            if (typeof rawVal === "number") {
                if (rawVal > 0 && r.colorize) value.classList.add("positive");
                if (rawVal < 0 && r.colorize) value.classList.add("negative");
            }

            row.appendChild(label);
            row.appendChild(value);
            container.appendChild(row);
        }
    }

    // ---- Chart rendering ----
    var chartInstance = null;

    function renderChart(chartData, canvasId) {
        if (!chartData) return;
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;

        var chartSection = canvas.closest(".chart-section");
        if (chartSection) chartSection.classList.add("visible");

        if (chartInstance) {
            chartInstance.destroy();
            chartInstance = null;
        }

        var ctx = canvas.getContext("2d");
        chartInstance = new Chart(ctx, chartData);
    }

    // ---- URL hash state ----
    function saveToHash(inputs) {
        var parts = [];
        for (var k in inputs) {
            if (inputs.hasOwnProperty(k)) {
                parts.push(encodeURIComponent(k) + "=" + encodeURIComponent(inputs[k]));
            }
        }
        history.replaceState(null, "", "#" + parts.join("&"));
    }

    function loadFromHash(formEl) {
        var hash = window.location.hash.substring(1);
        if (!hash) return;
        var pairs = hash.split("&");
        for (var i = 0; i < pairs.length; i++) {
            var kv = pairs[i].split("=");
            var key = decodeURIComponent(kv[0]);
            var val = decodeURIComponent(kv[1] || "");
            var field = formEl.querySelector('[name="' + key + '"]');
            if (field) {
                if (field.type === "checkbox") {
                    field.checked = (val === "true");
                } else {
                    field.value = val;
                }
            }
        }
    }

    // ---- Debounce ----
    function debounce(fn, delay) {
        var timer;
        return function() {
            clearTimeout(timer);
            timer = setTimeout(fn, delay);
        };
    }

    // ---- Main init ----
    window.initCalculator = function(config) {
        var formEl = document.getElementById("calc-form");
        var resultsContainer = document.getElementById("calc-results");
        var resultsSection = document.getElementById("results-section");
        var errorEl = document.getElementById("calc-error");
        var canvasId = config.canvasId || "calc-chart";

        if (!formEl || !resultsContainer) return;

        // Load hash state on page load
        loadFromHash(formEl);

        function runCalculation() {
            var inputs = readInputs(formEl);

            // Validate
            if (errorEl) errorEl.textContent = "";
            var err = validate(inputs, config.validation);
            if (err) {
                if (errorEl) {
                    errorEl.textContent = err;
                    errorEl.style.display = "block";
                }
                if (resultsSection) resultsSection.classList.remove("visible");
                return;
            }
            if (errorEl) errorEl.style.display = "none";

            // Run formula
            var output;
            try {
                output = config.calculate(inputs);
            } catch(e) {
                if (errorEl) {
                    errorEl.textContent = "Calculation error: " + e.message;
                    errorEl.style.display = "block";
                }
                return;
            }

            // Auto-detect return format: convert legacy {key: value} to {results: [...]}
            if (output && !output.results) {
                var autoResults = [];
                var rawChart = output.chart || output.chart_data || null;
                var keys = Object.keys(output);
                for (var k = 0; k < keys.length; k++) {
                    var key = keys[k];
                    if (key === 'chart' || key === 'chart_data') continue;
                    var val = output[key];
                    if (val === null || val === undefined) continue;
                    if (Array.isArray(val)) {
                        for (var a = 0; a < val.length; a++) {
                            var item = val[a];
                            if (item && typeof item === 'object' && item.label !== undefined) {
                                var av = item.value;
                                var af = typeof av === 'string' ? 'text' : (/cost|price|value|balance|payment/i.test(key) ? 'currency' : 'number');
                                autoResults.push({label: item.label, value: av, format: af, decimals: af === 'currency' ? 2 : (af === 'text' ? 0 : 1)});
                            }
                        }
                        if (!rawChart && val.length > 0 && val[0] && val[0].label !== undefined) {
                            rawChart = val;
                        }
                        continue;
                    }
                    if (typeof val === 'object' && val !== null) continue;
                    var lbl = key.replace(/_/g, ' ').replace(/\w/g, function(c) { return c.toUpperCase(); });
                    var ftype = 'number';
                    var dec = 2;
                    if (typeof val === 'string') {
                        ftype = 'text'; dec = 0;
                    } else if (/cost|price|value|budget|revenue|profit|salary|income|tax|fee|payment|balance|contribution|interest|savings/i.test(key)) {
                        ftype = 'currency';
                    } else if (/pct|percent|roi|margin/i.test(key) && Math.abs(val) < 200) {
                        ftype = 'percentage';
                    } else if (/count|needed|bags|rolls|pallets|pieces|blocks|pavers|bricks|applications|years|days|months|number|qty|quantity/i.test(key)) {
                        ftype = 'integer'; dec = 0;
                    }
                    autoResults.push({label: lbl, value: val, format: ftype, decimals: dec});
                }
                var chartConfig = null;
                if (rawChart) {
                    if (rawChart.type && rawChart.data) {
                        chartConfig = rawChart;
                    } else if (Array.isArray(rawChart) && rawChart.length > 0 && rawChart[0].label !== undefined) {
                        chartConfig = {
                            type: 'bar',
                            data: {
                                labels: rawChart.map(function(d) { return d.label; }),
                                datasets: [{
                                    label: 'Value',
                                    data: rawChart.map(function(d) { return typeof d.value === 'number' ? d.value : parseFloat(d.value) || 0; }),
                                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    borderWidth: 1
                                }]
                            },
                            options: { responsive: true, plugins: { legend: { display: false } } }
                        };
                    }
                }
                output = {results: autoResults, chart: chartConfig};
            }

            // Display results
            displayResults(output.results, resultsContainer);
            if (resultsSection) resultsSection.classList.add("visible");

            // Normalize simplified chart format {type, labels, values} to full Chart.js
            if (output.chart && output.chart.labels && output.chart.values && !output.chart.data) {
                output.chart = {
                    type: output.chart.type || 'bar',
                    data: {
                        labels: output.chart.labels,
                        datasets: [{
                            label: 'Value',
                            data: output.chart.values,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { display: false } } }
                };
            }

            // Render chart
            if (output.chart) {
                renderChart(output.chart, canvasId);
            }

            // Update hash
            saveToHash(inputs);
        }

        // Button click
        var btn = document.getElementById("btn-calculate");
        if (btn) {
            btn.addEventListener("click", function(e) {
                e.preventDefault();
                runCalculation();
            });
        }

        // Debounced auto-calculate on input change
        var autoCalc = debounce(runCalculation, 500);
        formEl.addEventListener("input", autoCalc);
        formEl.addEventListener("change", autoCalc);

        // If hash had values, auto-calculate on load
        if (window.location.hash.length > 1) {
            runCalculation();
        }
    };
})();
