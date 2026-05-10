import requests
from behave import given
from service.common import status

@given('the following products')
def step_impl(context):
    """Delete all Products and load new ones"""
    # 1. Tentukan endpoint API
    rest_endpoint = f"{context.base_url}/products"
    
    # 2. Ambil semua produk yang ada saat ini
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == status.HTTP_200_OK
    
    # 3. Hapus semua produk lama agar database bersih
    for product in context.resp.get_json():
        requests.delete(f"{rest_endpoint}/{product['id']}")
        
    # 4. Masukkan data baru dari tabel Gherkin
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == status.HTTP_201_CREATED
