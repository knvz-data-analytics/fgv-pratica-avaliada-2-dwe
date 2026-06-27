from typing import Optional
from sqlalchemy import String, Float, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# 1. Modelo definido

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
    
# 2. Confiração do SqlAlchemy com SQLite Local
engine = create_engine("sqlite:///products.db", echo=False)

# Crias as tabelas no banco
Base.metadata.create_all(bind=engine)

# 3. Gerenciamento de Sessão
# Cria uma 'fábrica' de sessão vincluda a configuração do SqlAlchemy 'engine'
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Operações de CRUD

def create_product(name: str, price: float, description: str = None):
    """CREATE: Adiciona um novo produto ao banco"""
    # with: garante o gerenciamento da sessão (abertura/fechamento auto)
    with SessionLocal() as session:
        new_product = Product(name=name, price=price, description=description)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        print(F"[CREATE] Produto '{new_product.name}' criado com sucesso! ID: {new_product.id}")
        return new_product
    
def read_all_products():
    """READ: Retorna todos os produtos"""
    with SessionLocal() as session:
        stmt = select(Product)
        products = session.scalars(stmt).all()
        print(f"[READ] Produtos encontrados: {products}")
        return products
    
def update_product_price(product_id: int, new_price: float):
    """UPDATE: Atualiza o preço de um produto existente."""
    with SessionLocal() as session:
        product = session.get(Product, product_id)
        if product:
            product.price = new_price
            session.commit()
            print(f"[UPDATE] Preço do produto ID {product_id} atualizado para {new_price}.")
        else:
            print(f"[UPDATE] Produto ID {product_id} não encontrado.")

def delete_produto(product_id: int):
    """DELETE: Remove o produto do banco."""
    with SessionLocal() as session:
        product = session.get(Product, product_id)
        if product:
            session.delete(product)
            session.commit()
            print(f"[DELETE] Produto ID {product_id} deletado com sucesso.")
        else:
            print(f"[DELETE] Produto ID {product_id} não econtrado.")
            
# Testantdo API (CRUDs)
if __name__ == "__main__":
    print("*** Iniciando testes do CRUD ***")
    
    # 1. Create
    create_product("Teclado Mecânico HyperX", 350.00, "Teclado RG switch blue")
    create_product("Teclado Mecânico Red Dragon", 325.00, "Teclado RG switch red")
    
    # 2. Read
    read_all_products()
    
    # 3. Update
    update_product_price(1, 400.00) # Mudando o preço do teclado com ID: 1
    
    # 4. Read (Ver o ponto anterior)
    read_all_products()
    
    # 5. Delete
    delete_produto(2)
    
    # 6. Read Final
    read_all_products()