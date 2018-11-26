import csv
import urllib.request as urllib2
from urllib.request import Request, urlopen
import base64
import io
import sys
import flectra
from flectra import models, fields, api
from flectra.exceptions import Warning


class ProductImageImportWizard(models.TransientModel):
    _name = 'import.product_image'

    product_model = fields.Selection([('1', 'Product Template')], string="Product Model")
    pdt_operation = fields.Selection([('2', 'Product Updation')], string="Product Operation")
    file = fields.Binary('File to import', required=True)
    images = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Images')
    
    @api.multi
    def import_file(self):
        image_ar = self.env['ir.attachment']
        file = io.StringIO(base64.decodestring(self.file).decode('ascii'))
        # file = open(self.file.decode('ascii'), 'rb')
        reader = csv.reader(file, delimiter=',')
        csv.field_size_limit(sys.maxsize)
        skip_header = True
        for row in reader:
            if skip_header:
                index_image = int(row.index('image'))
                index_name  = int(row.index('name'))
                skip_header = False
                continue

            product = row[index_name]
            image_path = row[index_image]
            
            if "http://" in image_path or "https://" in image_path:
                try:
                    # link = urllib2.urlopen(image_path).read()
                    link = urlopen(Request(image_path, headers={'User-Agent': 'Mozilla/5.0'})).read()
                    image_base64 = base64.encodestring(link)
                    if self.product_model == '1':
                        product_obj = self.env['product.template']
                    else:
                        product_obj = self.env['product.product']
                    product_id = product_obj.search([('name', '=', product)])

                    vals = {
                        'image_medium': image_base64,
                        'name': product,
                    }
                    if self.pdt_operation == '1' and not product_id:
                        product_obj.create(vals)
                    elif self.pdt_operation == '1' and product_id:
                        product_id.write(vals)
                    elif self.pdt_operation == '2' and product_id:
                        product_id.write(vals)
                    elif not product_id and self.pdt_operation == '2':
                        raise Warning("Could not find the product '%s'" % product)
                except:
                    raise Warning("Please provide correct URL for product '%s' or check your image size.!" % product)
            else:
                try:
                    # with open(image_path, 'rb') as image:
                    # base64data   = base64.b64encode(image.read())
                    # image_base64 = base64data
                    # if self.product_model == '1':
                    image           =   ""
                    image_medium    =   ""
                    image_small     =   ""

                    for img in self.images.filtered(lambda img: img.name == image_path):
                        image        = img[0].datas
                        image_medium = flectra.tools.image_resize_image(base64_source=img[0].datas, size=(128, 128), encoding='base64', filetype='PNG')
                        image_small  = flectra.tools.image_resize_image(base64_source=img[0].datas, size=(64, 64), encoding='base64', filetype='PNG')


                    product_obj = self.env['product.template']
                    # else:
                    #     product_obj = self.env['product.product']
                    product_id = product_obj.search([('name', '=', product)])

                    vals = {
                        'image_medium': '',
                        'image_small': '',
                        'image': '',
                        'name': product,
                    }

                    product_id.write(vals)

                    edit  = image_ar.search([('name', '=', image_path)])
    
                    for e in edit:
                        value1   =   {
                            'name': e[0]['name'],
                            'public': True,
                            'datas_fname': e[0]['datas_fname'],
                            'res_model': 'product.template',
                            'res_field': 'image_small',
                            'res_id': product_id[0]['id'],
                            'create_uid': e[0]['create_uid'][0]['id'],
                            'company_id': e[0]['company_id'][0]['id'],
                            'type': e[0]['type'],
                            'public': True,
                            'datas': image_small,
                            'index_content': e[0]['index_content'],
                            'write_uid': e[0]['write_uid'],
                        }
                        value2   =   {
                            'name': e[0]['name'],
                            'public': True,
                            'datas_fname': e[0]['datas_fname'],
                            'res_model': 'product.template',
                            'res_field': 'image',
                            'res_id': product_id[0]['id'],
                            'create_uid': e[0]['create_uid'][0]['id'],
                            'company_id': e[0]['company_id'][0]['id'],
                            'type': e[0]['type'],
                            'public': True,
                            'datas': image,
                            'index_content': e[0]['index_content'],
                            'write_uid': e[0]['write_uid'],
                        }
                        value3   =   {
                            'name': e[0]['name'],
                            'public': True,
                            'datas_fname': e[0]['datas_fname'],
                            'res_model': 'product.template',
                            'res_field': 'image_medium',
                            'res_id': product_id[0]['id'],
                            'create_uid': e[0]['create_uid'][0]['id'],
                            'company_id': e[0]['company_id'][0]['id'],
                            'type': e[0]['type'],
                            'public': True,
                            'datas': image_medium,
                            'index_content': e[0]['index_content'],
                            'write_uid': e[0]['write_uid'],
                        }
                        value4   =   {
                            'name': e[0]['name'],
                            'public': True,
                            'datas_fname': e[0]['datas_fname'],
                            'res_model': 'product.template',
                            'res_field': None,
                            'res_id': product_id[0]['id'],
                            'create_uid': e[0]['create_uid'][0]['id'],
                            'company_id': e[0]['company_id'][0]['id'],
                            'type': e[0]['type'],
                            'public': True,
                            'datas': image,
                            'index_content': e[0]['index_content'],
                            'write_uid': e[0]['write_uid'],
                        }
                    
                    image_ar.create(value1)
                    image_ar.create(value2)
                    image_ar.create(value3)
                    image_ar.create(value4)

                    # vals = {
                    #     'image_medium': image_base64,
                    #     'name': product,
                    # }
                    # if self.pdt_operation == '1' and not product_id:
                    #     product_obj.create(vals)
                    # elif self.pdt_operation == '1' and product_id:
                    #     product_id.write(vals)
                    # elif self.pdt_operation == '2' and product_id:
                    #     product_id.write(vals)
                    # elif not product_id and self.pdt_operation == '2':
                    #     raise Warning("Could not find the product '%s'" % product)
                except IOError:
                    raise Warning("Could not find the image '%s' - please make sure it is accessible to this script" %
                                  product)
