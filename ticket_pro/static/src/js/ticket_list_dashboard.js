/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useRef, onMounted, onWillUnmount } from "@odoo/owl";

export class TicketListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        this.rootRef = useRef("root");
        
        onMounted(() => {
            this.loadDashboard();
        });

        onWillUnmount(() => {
            this.cleanupDashboard();
        });
    }

    async loadDashboard() {
        if (!this.dashboardValues) {
            this.dashboardValues = await this.orm.call(
                "ticket.pro",
                "retrieve_dashboard",
                []
            );
            await this.renderDashboard();
        }
    }

    async renderDashboard() {
        if (this.dashboardValues && this.rootRef.el) {
            const dashboardHtml = await this.env.services.rpc({
                route: "/web/dataset/call_kw/ir.qweb/render",
                params: {
                    model: "ir.qweb",
                    method: "render",
                    args: ["ticket_pro.TicketDashboard", { values: this.dashboardValues }],
                    kwargs: {},
                },
            });

            this.rootRef.el.innerHTML = dashboardHtml;
            this.setupDashboardEvents();
        }
    }

    cleanupDashboard() {
        if (this.rootRef.el) {
            this.rootRef.el.innerHTML = "";
        }
    }

    setupDashboardEvents() {
        if (this.rootRef.el) {
            const actions = this.rootRef.el.querySelectorAll(".o_dashboard_action");
            actions.forEach(action => {
                action.addEventListener("click", async (ev) => {
                    ev.preventDefault();
                    const context = action.getAttribute("context");
                    if (context) {
                        await this.action.doAction("ticket_pro.action_ticket_pro", {
                            additionalContext: JSON.parse(context),
                        });
                    }
                });
            });
        }
    }
}

TicketListController.template = "ticket_pro.ListController";
TicketListController.components = { ...ListController.components };

registry.category("views").add("ticket_list_dashboard", {
    ...listView,
    Controller: TicketListController,
}); 