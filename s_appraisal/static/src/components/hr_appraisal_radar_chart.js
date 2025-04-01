/** @odoo-module **/

import {registry} from "@web/core/registry";
import {ChartRenderer} from "./chart_renderer";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {useState, Component, onWillStart} from "@odoo/owl";

export class AppraisalRadarChart extends Component {
    setup() {
        this.actionService = useService("action");
        this.state = useState({
            chartData: {
                labels: [],
                datasets: []
            }
        });

        onWillStart(async () => {
            await this.loadChartData();
        });
    }

    async loadChartData() {
        const actionContext = this.props.action.context;

        if (actionContext) {
            if (actionContext.data && actionContext.data.length > 0) {
                if (actionContext.data[0].labels) {
                    this.state.chartData.labels = actionContext.data[0].labels.map(label => {
                        const maxCharsPerLine = 40;

                        if (label.length <= maxCharsPerLine) {
                            return label;
                        }

                        const words = label.split(' ');
                        const lines = [];
                        let currentLine = '';

                        for (let i = 0; i < words.length; i++) {
                            const word = words[i];

                            if ((currentLine + ' ' + word).length <= maxCharsPerLine || currentLine.length === 0) {
                                currentLine += (currentLine.length > 0 ? ' ' : '') + word;
                            } else {
                                lines.push(currentLine);
                                currentLine = word;
                            }
                        }

                        if (currentLine.length > 0) {
                            lines.push(currentLine);
                        }

                        return lines;
                    });
                }

                this.state.chartData.datasets = actionContext.data.map((employeeData, index) => {
                    const colors = [
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ];

                    const borderColors = [
                        'rgb(54, 162, 235)',
                        'rgb(255, 99, 132)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)',
                        'rgb(255, 159, 64)'
                    ];

                    const backgroundColor = colors[index % colors.length];
                    const borderColor = borderColors[index % borderColors.length];

                    return {
                        label: _t(`Review of `) + `${employeeData.name}`,
                        data: employeeData.scores,
                        fill: true,
                        backgroundColor: backgroundColor,
                        borderColor: borderColor,
                        pointBackgroundColor: borderColor,
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: borderColor
                    };
                });
            }
        }
    }

    goBackAction() {
        window.history.back();
    }
}

AppraisalRadarChart.template = "s_appraisal.AppraisalRadarChart";
AppraisalRadarChart.components = {ChartRenderer};

registry.category("actions").add("s_appraisal.hr_appraisal_radar_chart", AppraisalRadarChart);
