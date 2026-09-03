from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class RegisterIn(BaseModel): name: str = Field(min_length=2, max_length=120); email: EmailStr; password: str = Field(min_length=6, max_length=128)
class LoginIn(BaseModel): email: EmailStr; password: str
class UserOut(BaseModel): model_config = ConfigDict(from_attributes=True); id: int; name: str; email: EmailStr; role: str; is_active: bool; is_approved: bool; created_at: datetime
class TokenOut(BaseModel): access_token: str; token_type: str = 'bearer'; user: UserOut
class CategoryIn(BaseModel): name: str = Field(min_length=1, max_length=100); description: str | None = None
class CategoryOut(CategoryIn): model_config = ConfigDict(from_attributes=True); id: int; created_at: datetime
class ProductIn(BaseModel): name: str = Field(min_length=1, max_length=200); article_number: str | None = None; barcode: str | None = None; category_id: int | None = None; purchase_price: float = Field(default=0, ge=0); sale_price: float = Field(default=0, ge=0); quantity: int = Field(default=0, ge=0); min_quantity: int = Field(default=0, ge=0); description: str | None = None; image: str | None = None
class ProductOut(ProductIn): model_config = ConfigDict(from_attributes=True); id: int; owner_id: int; created_at: datetime; updated_at: datetime
class ProductPage(BaseModel): items: list[ProductOut]; total: int; limit: int; offset: int
class BatchIn(BaseModel): batch_number: str | None = None; boxes: int = Field(gt=0); items_per_box: int = Field(gt=0)
class BatchOut(BatchIn): model_config = ConfigDict(from_attributes=True); id: int; product_id: int; total_quantity: int; created_at: datetime
class QuantityIn(BaseModel): product_id: int; quantity: int = Field(gt=0)
class SaleOut(BaseModel): model_config = ConfigDict(from_attributes=True); id: int; product_id: int; user_id: int; quantity: int; price: float; total_amount: float; created_at: datetime
