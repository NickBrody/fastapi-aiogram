from pydantic import BaseModel


class BaseProduct(BaseModel):

    articul: int


class ProductIn(BaseProduct):
    ...

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    name: str
    articul: int
    price: float
    rating: int
    total: int

    class Config:
        orm_mode = True  

# class RecipeOut(BaseRecipe):
#     id: int

#     class Config:
#         orm_mode = True


# class BaseAllRecipe(BaseModel):
#     """
#     Базовый класс для всех рецептов
#     """
#     title: str
#     time: int
#     ingredients: str
#     description: str


# class AllRecipeIn(BaseAllRecipe):
#     ...


# class AllRecipeOut(BaseAllRecipe):
#     id: int

#     class Config:
#         orm_mode = True