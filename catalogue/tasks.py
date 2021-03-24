from catalogue.models import Product, PurchaseStatus
from contracts_api import ContractWrapper
from smartcontract.settings import INFURA_KEYY
from smartcontract import celery_app


@celery_app.task
def submit_new_smart_contract(seller_hash, solver_hash, buyer_private_key, price, product_id):
    wrapper = ContractWrapper(INFURA_KEYY, buyer_private_key, timeout=600)  # default timeout value is 600

    seller_address = seller_hash
    solver_address = solver_hash

    product_obj = Product.objects.get(id=product_id)

    result = wrapper.create(
        seller_address,  # str
        solver_address,  # str
        int(float(price)),  # price of the product: should be int
        str(product_id)  # product id: should be int casted to string
    )
    product_obj.contract_address = result["receipt"]["contractAddress"]
    product_obj.status = PurchaseStatus.ORDER
    product_obj.save()


@celery_app.task
def send_product(solver_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEYY, solver_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    result = wrapper.send(
        contract_address,  # smart contract address: str
    )
    product_obj.status = PurchaseStatus.SENT
    product_obj.save()


@celery_app.task
def receive_product(buyer_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEYY, buyer_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    wrapper.confirm(
        contract_address,  # smart contract address: str
    )
    product_obj.status = PurchaseStatus.RECEIVED
    product_obj.save()