/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TicketDashboard extends Component {
    setup() {
        this.values = this.props.values;
    }
}

TicketDashboard.template = "ticket_pro.TicketDashboard"; 