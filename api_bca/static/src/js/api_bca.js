function rupiah(bilangan = 0) {
    var	number_string = bilangan.toString(),
        sisa 	= number_string.length % 3,
        rupiah 	= number_string.substr(0, sisa),
        ribuan 	= number_string.substr(sisa).match(/\d{3}/g);
            
    if (ribuan) {
        separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }

    return rupiah
}

flectra.define('api.bca', function(require) {
    "use strict";

    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var KanbanView = require('web.KanbanView');
    var KanbanModel = require('web.KanbanModel');
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanController = require('web.KanbanController');
    var data = require('web.data');
    var view_registry = require('web.view_registry');
    var QWeb = core.qweb;

    var _t = core._t;
    var _lt = core._lt;

    var ApiBcaRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            "click #reset": "render_balance",
            "click #search": "render_transaction"
        }),


        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Notifies the controller that the target has changed.
         *
         * @private
         * @param {string} target_name the name of the changed target
         * @param {string} value the new value
         */
        _notifyTargetChange: function (target_name, value) {
            this.trigger_up('dashboard_edit_target', {
                target_name: target_name,
                target_value: value,
            });
        },

        fetch_data: function() {
            // Overwrite this function with useful data
            return $.when();
        },
        /**
         * @override
         * @private
         * @returns {Deferred}
         */
        _render: function() {
            var super_render = this._super;
            var self = this;
            self._rpc({
                route: '/api_bca/partner_bank',
                params: {},}).done(function
            (result) {
                result.forEach((v) => {
                    $("#bank_content").append(`
                        <option value="${ v["id"] }">${ v["name"] }</option>
                    `)
                })

                $(".date").daterangepicker({
                    initialText : 'Periode Date',
                });
            });

            self.render_balance()
            
            return this.fetch_data().then(function(result) {
                var tes_dashboard_view = QWeb.render('ApiBca');
                super_render.call(self);
                $(tes_dashboard_view).prependTo(self.$el);
            });
        },

        render_balance: function() {
            let self    =   this

            self._rpc({
                route: '/api_bca/get_balance',
                params: {},}).done(function
            (result) {
                $("#table-balance").empty()
                $("#head-table").empty()

                $("#head-table").append(`
                    <tr>
                        <th>Account Number</th>
                        <th>Currency</th>
                        <th>Balance</th>
                        <th>Available Balance</th>
                        <th>Float Amount</th>
                        <th>Hold Amount</th>
                        <th>Plafon</th>
                    </tr>
                `)

                result.forEach((v) => {
                    $("#table-balance").append(`
                        <tr>
                            <td>${ v.AccountNumber }</td>
                            <td>${ v.Currency }</td>
                            <td>Rp. ${ rupiah(v.Balance) }</td>
                            <td>Rp. ${ rupiah(v.AvailableBalance) }</td>
                            <td>Rp. ${ rupiah(v.FloatAmount) }</td>
                            <td>Rp. ${ rupiah(v.HoldAmount) }</td>
                            <td>Rp. ${ rupiah(v.Plafon) }</td>
                        </tr>
                    `)
                })

                $(".table").DataTable()
            });
        },

        render_transaction: function() {
            if($(".date").val() == "") {
                alert('periode harap diisi')
                return false
            }
            
            let self    = this,
                date    = JSON.parse($(".date").val()) || $(".date").val(),
                start   = date.start || "2016-08-29",
                end     = date.end || "2016-09-01",
                number  = $("#bank_content").val()

            self._rpc({
                route: `/api_bca/get_transaction/${ number }/${ start }/${ end }`,
                params: {},}).done(function
            (result) {
                let data    =   result.Data

                $("#table-balance").empty()
                $("#head-table").empty()

                $("#head-table").append(`
                    <tr>
                        <th>Branch Code</th>
                        <th>Trailer</th>
                        <th>Transaction Amount</th>
                        <th>Transaction Date</th>
                        <th>Transaction Name</th>
                        <th>Transaction Type</th>
                    </tr>
                `)
                
                if(result['ErrorCode'] == undefined) {
                    data.forEach((v) => {
                        $("#table-balance").append(`
                            <tr>
                                <td>${ v.BranchCode }</td>
                                <td>${ v.Trailer }</td>
                                <td>Rp. ${ rupiah(v.TransactionAmount) }</td>
                                <td>${ v.TransactionDate }</td>
                                <td>${ v.TransactionName }</td>
                                <td>${ v.TransactionType }</td>
                            </tr>
                        `)
                    })
                } else {
                    $("#table-balance").append(`
                        <tr>
                            <td class="text-center" colspan="6">${ (result['ErrorMessage']['indonesia'] != undefined) ? result['ErrorMessage']['indonesia'] : "Tidak ada record transaksi" }</td>
                        </tr>
                    `)
                }

                $(".table").DataTable()
            });
        }

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        
    });

    var ApiBcaModel = KanbanModel.extend({
        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        init: function () {
            this.dashboardValues = {};
            this._super.apply(this, arguments);
        },

        /**
         * @override
         */
        get: function (localID) {
            var result = this._super.apply(this, arguments);
            return result;
        },


        /**
         * @œverride
         * @returns {Deferred}
         */
        load: function () {
            return this._super.apply(this, arguments);
        },
        /**
         * @œverride
         * @returns {Deferred}
         */
        reload: function () {
            return this._super.apply(this, arguments);
        },
    });

    var ApiBcaController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: ApiBcaModel,
            Renderer: ApiBcaRenderer,
            Controller: ApiBcaController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('api_bca', MyMainDashboard);

    return {
        Model: ApiBcaModel,
        Renderer: ApiBcaRenderer,
        Controller: ApiBcaController,
    };
});
    