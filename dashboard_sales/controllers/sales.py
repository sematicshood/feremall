from flectra import http
from flectra.http import request
from datetime import datetime
from . import lib_function as f
from . import functions as fu
from itertools import groupby
from operator import itemgetter

class LibraryExample(http.Controller):
    @http.route('/sales_dashboard/total_sales_product_chart/<branch>/<start>/<end>', type='json')
    def total_sales_produk(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        total_sales   =   0
        total_ids     =   request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                        ('invoice_status', '=', 'invoiced'),
                                                        ('create_date', '>=', start),
                                                        ('create_date', '<=', end)])

        try:
            for d in total_ids:
                total_sales += d.price_total
            
            value.append({
                'Total Sales Produk': total_sales
            })
        except Exception as e:
            pass

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/sales_dashboard/total_sales_group_product_chart/<branch>/<start>/<end>', type='json')
    def total_sales_group_produk(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   {}
        total   =   0
        categ_id = []
        total_ids     =   request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                        ('create_date', '>=', start),
                                                        ('create_date', '<=', end)])
        
        def cek(a, b):
            condition = False
            for i in a:
                if i[0] == b:
                    condition = True
            return condition

        list_data = [{
            'price_total':d.price_total,
            'id_categ':d.product_id.categ_id
        }for d in total_ids]

        for d in list_data:
            if cek(categ_id, d['id_categ']) is False:
                categ_id.append([d['id_categ'], 0])

        for idx, d in enumerate(categ_id):
            for i in list_data:
                if d[0] == i['id_categ']:
                    categ_id[idx][1] += i['price_total']

        for d in categ_id:
            value['{key}'.format(key=d[0].name)] = d[1]

        data.append({
            'labels': labels, 
            'value': [value]
        })

        return data

    @http.route('/sales_dashboard/total_margin_chart/<branch>/<start>/<end>', type='json')
    def total_margin(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        total_lst_price = 0
        total_standard_price = 0
        total_sales = 0
        margin = 0
        total_margin = 0
        
        try:
            total_sales_data = request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                            ('invoice_status', '=', 'invoiced'),
                                                            ('create_date', '>=', start),
                                                            ('create_date', '<=', end)])
            

            # jadi list_price - standard_price= margin 
            # margin x total product terjual  = total margin
            # %margin = total_margin/total_sales

            def cek(a,b):
                condition = False
                for i in a:
                    if i == b:
                        condition = True
                return condition

            for d in total_sales_data:
                total_margin += (d.product_id.list_price - d.product_id.standard_price) * d.product_uom_qty                                  
                total_sales += d.price_total                
            
            print(total_margin, total_sales)
            margin = total_margin / total_sales * 100.0

            print(total_margin)

            value.append({
                'Total Margin ({key}%)'.format(key=("%.2f" % margin)): total_margin
            })
        except Exception as e:
            pass

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/sales_dashboard/total_margin_sales_chart/<branch>/<start>/<end>', type='json')
    def total_margin_sales(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        total_lst_price = 0
        total_standard_price = 0
        total_sales = 0
        margin = 0
        total_margin = 0
        
        try:
            total_sales_data = request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                            ('invoice_status', '=', 'invoiced'),
                                                            ('create_date', '>=', start),
                                                            ('create_date', '<=', end)])
            

            # jadi list_price - standard_price= margin 
            # margin x total product terjual  = total margin
            # %margin = total_margin/total_sales

            def cek(a,b):
                condition = False
                for i in a:
                    if i == b:
                        condition = True
                return condition

            for d in total_sales_data:
                total_margin += (d.product_id.list_price - d.product_id.standard_price) * d.product_uom_qty                                  
                total_sales += d.price_total                
            
            print(total_margin, total_sales)
            margin = total_margin / total_sales * 100.0

            print(total_margin)

            value.append({
                'Total Sales': total_sales,
                'Total Margin': total_margin
            })
        except Exception as e:
            pass

        data.append({
            'labels': labels, 
            'value': value,
            'margin': ("%.2f" % margin)
        })

        return data


    @http.route('/sales_dashboard/top_product_sales_chart/<branch>/<start>/<end>', type='json')
    def top_product_sales(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)        
        list_no_bulan = f.month_to_number(start, end)
        value   =   {}
        categ_id = []
        categ_id_month = []
        main_data = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]

        total_ids     =   request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                        ('create_date', '>=', start),
                                                        ('create_date', '<=', end)], order="price_total desc")
        
        
        
        #tentukan 10 barang tertinggi
        # 1. get data dari database
        list_data = [{
            'price_total':d.price_total,
            'id_product':d.product_id.id,
            'name':d.name,
            'bulan':f.date_to_month_number(d.create_date)
        }for d in total_ids]

        # 2. grouping data berdasarkan id_produk
        def cek_group_by_id(a, b):
            condition = False
            for i in a:
                if i[0] == b:
                    condition = True
            return condition

        for d in list_data:
            if cek_group_by_id(categ_id, d['id_product']) is False:
                categ_id.append([d['id_product'], 0, d['name']])

        # 3. Jumlahkan price total pada id_produk yang sama
        for idx, d in enumerate(categ_id):
            for i in list_data:
                if d[0] == i['id_product']:
                    categ_id[idx][1] += i['price_total']
        
        # 4. limit 10 data tertinggi nilai price totalnya
        top_ten_data = []
        for d in range(10):
            try:
                top_ten_data.append([categ_id[9-d][0], categ_id[9-d][2]])
                # value['{key}'.format(key=categ_id[9-d][2])] = categ_id[9-d][1]
            except Exception as e:
                pass

        # 5. buat list untuk label atas
        label_atas = []
        for v in top_ten_data:
            label_atas.append(v[1])
            
        # 6. buat grouping data berdasarkan id_produk dan bulan
        def cek_group_by_id_and_month(a, b, c):
            condition = False
            for i in a:
                if i[0] == b and i[3] == c:
                    condition = True
            return condition

        for d in list_data:
            if cek_group_by_id_and_month(categ_id_month, d['id_product'], d['bulan']) is False:
                categ_id_month.append([d['id_product'], 0, d['name'], d['bulan']])

        # 7. Jumlahkan price total pada id_produk dan bulan yang sama
        for idx, d in enumerate(categ_id_month):
            for i in list_data:
                if d[0] == i['id_product'] and d[3] == i['bulan']:
                    categ_id_month[idx][1] += i['price_total']

        # 9. buat list data berdasarkan loop dari label_atas (nama produk)
        for i, d in enumerate(label_atas):
            for j, b in enumerate(list_no_bulan):
                isi = False               
                for c in categ_id_month:
                    if d == c[2] and b == c[3]:
                        main_data[i].append(c[1])
                        isi = True
                if isi == False:    
                    main_data[i].append(0)

        # 10. Mapping data
        for d in range(10):
            try:
                value['{key}'.format(key=label_atas[d])] = main_data[d]
            except Exception as e:
                pass

        data.append({
            'labels': labels, 
            'value': [value]
        })
        return data

        # def cek2(a, b, c):
        #     condition = False
        #     for i in a:
        #         if i[0] == b and i[3] == c:
        #             condition = True
        #     return condition

        # list_data = [{
        #     'price_total':d.price_total,
        #     'id_product':d.product_id.id,
        #     'name':d.name,
        #     'bulan':f.date_to_month_number(d.create_date)
        # }for d in total_ids]

        # for d in list_data:
        #     if cek2(categ_id, d['id_product'], d['bulan']) is False:
        #         categ_id.append([d['id_product'], 0, d['name'], d['bulan']])

        # # print(categ_id)
        # for idx, d in enumerate(categ_id):
        #     for i in list_data:
        #         if d[0] == i['id_product'] and d[3] == i['bulan']:
        #             categ_id[idx][1] += i['price_total']
        

        # # print(categ_id)  

        # # for d in range(10):
        # #     try:
                
        # #     except Exception as e:
        # #         print(str(e)) 

        # value_a = [
        #     [36, 3640000.0, '[CONS_DEL02] Little server\nraid 1, 512ECC ram', 10], 
        #     [37, 360173.0, '[CONS_DEL01] Server\nraid 10, 2048ECC ram', 11], 
        #     [35, 258500.0, '[CONS_DEL03] Basic Computer\nDvorak keyboard\nleft-handed mouse', 11], 
        #     [33, 53100.0, 'Laptop E5023', 10], [36, 160450.0, '[CONS_DEL02] Little server\nraid 1, 512ECC ram', 11], 
        #     [35, 47000.0, '[CONS_DEL03] Basic Computer\nDvorak keyboard\nleft-handed mouse', 10], 
        #     [33, 37550.0, 'Laptop E5023', 11], [34, 9735.0, 'Laptop Customized', 11], 
        #     [34, 7290.0, 'Laptop Customized', 10], 
        #     [31, 6300.0, '[CPUi5] Processor Core i5 2.70 Ghz', 11]
        # ]

        # # value_b = [
        # #     {[{''},{},{}]},
        # #     {[{},{},{}]},
        # #     {[{},{},{}]},
        # #     {[{},{},{}]},
        # #     {[{},{},{}]},
        # #     {[{},{},{}]}
        # # ]

        # for d in range(10):
        #     try:
        #         value['{key}'.format(key=categ_id[9-d][2])] = categ_id[9-d][1]
        #     except Exception as e:
        #         pass

        # # print(value)

        

    @http.route('/sales_dashboard/top_product_sales_by_margin_chart/<branch>/<start>/<end>', type='json')
    def top_product_sales_by_margin(self, branch, start, end):
        data    =   []
        labels  =   f.month(start, end)
        list_no_bulan = f.month_to_number(start, end)
        value   =   {}
        categ_id = []
        categ_id_month = []
        main_data = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
        
        total_ids     =   request.env['sale.order.line'].search([('branch_id', '=', int(branch)),
                                                        ('create_date', '>=', start),
                                                        ('create_date', '<=', end)])
        
        # print("LIST NO BULAN")
        # print(list_no_bulan)

        #tentukan 10 barang tertinggi
        # 1. get data dari database
        list_data = [{
            'lst_price':d.product_id.lst_price,
            'standard_price':d.product_id.standard_price,
            'id_product':d.product_id.id,
            'name':d.name,
            'bulan':f.date_to_month_number(d.create_date)
        }for d in total_ids]

        # 2. grouping data berdasarkan id_produk
        def cek_group_by_id(a, b):
            condition = False
            for i in a:
                if i[0] == b:
                    condition = True
            return condition
        
        for d in list_data:
            if cek_group_by_id(categ_id, d['id_product']) is False:
                categ_id.append([d['id_product'], 0, d['name']])

        # 3. Jumlahkan margin pada id_produk yang sama
        for idx, d in enumerate(categ_id):
            for i in list_data:
                if d[0] == i['id_product']:
                    categ_id[idx][1] += (i['lst_price'] - i['standard_price'])

        # 4. limit 10 data tertinggi nilai marginnya
        top_ten_data = []
        for d in range(10):
            try:
                top_ten_data.append([categ_id[d][0], categ_id[d][2]])
                # value['{key}'.format(key=categ_id[9-d][2])] = categ_id[9-d][1]
            except Exception as e:
                pass

        # 5. buat list untuk label atas
        label_atas = []
        for v in top_ten_data:
            label_atas.append(v[1])
        
        # 6. buat grouping data berdasarkan id_produk dan bulan
        def cek_group_by_id_and_month(a, b, c):
            condition = False
            for i in a:
                if i[0] == b and i[3] == c:
                    condition = True
            return condition

        for d in list_data:
            if cek_group_by_id_and_month(categ_id_month, d['id_product'], d['bulan']) is False:
                categ_id_month.append([d['id_product'], 0, d['name'], d['bulan']])

        # 7. Jumlahkan margin pada id_produk dan bulan yang sama
        for idx, d in enumerate(categ_id_month):
            for i in list_data:
                if d[0] == i['id_product'] and d[3] == i['bulan']:
                    categ_id_month[idx][1] += (i['lst_price'] - i['standard_price'])

        # 9. buat list data berdasarkan loop dari label_atas (nama produk)
        for i, d in enumerate(label_atas):
            for j, b in enumerate(list_no_bulan):
                isi = False               
                for c in categ_id_month:
                    if d == c[2] and b == c[3]:
                        main_data[i].append(c[1])
                        isi = True
                if isi == False:    
                    main_data[i].append(0)

        # 10. Mapping data
        for d in range(10):
            try:
                value['{key}'.format(key=label_atas[d])] = main_data[d]
            except Exception as e:
                pass
        # print(value)   

        data.append({
            'labels': labels, 
            'value': [value]
        })
        return data

        # def cek2(a, b):
        #     condition = False
        #     for i in a:
        #         if i[0] == b:
        #             condition = True
        #     return condition
            
        # list_data = [{
        #     'lst_price':d.product_id.lst_price,
        #     'standard_price':d.product_id.standard_price,
        #     'id_product':d.product_id.id,
        #     'name':d.name
        # }for d in total_ids]

        # for d in list_data:
        #     if cek2(categ_id, d['id_product']) is False:
        #         categ_id.append([d['id_product'], 0, d['name']])
                
        # for idx, d in enumerate(categ_id):
        #     for i in list_data:
        #         if d[0] == i['id_product']:
        #             categ_id[idx][1] += (i['lst_price'] - i['standard_price'])

        # for d in range(10):
        #     try:
        #         value['{key}'.format(key=categ_id[d][2])] = categ_id[d][1]
        #     except Exception as e:
        #         pass            

        

    @http.route('/sales_dashboard/example_two/<start>/<end>', type='json')
    def get_exmample(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/sales_dashboard/example_three/<start>/<end>', type='json')
    def get_exmample_three(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/sales_dashboard/example_pie/<start>/<end>', type='json')
    def get_exmample_pie(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data