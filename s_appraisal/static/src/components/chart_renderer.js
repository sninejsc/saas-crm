/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { Component, useRef, onMounted, onWillUpdateProps, onWillStart } from "@odoo/owl";

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart");

        onWillStart(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js");
        });

        onWillUpdateProps(() => {
            this.renderChart();
        });

        onMounted(() => this.renderChart());
    }

    renderChart() {
        if (!this.props.data || !this.chartRef.el) return;

        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        this.chartInstance = new Chart(this.chartRef.el, {
            type: "radar",
            data: this.props.data,
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                }
            }
        });
    }
}

ChartRenderer.template = "s_appraisal.ChartRenderer";
ChartRenderer.props = ["data"];
