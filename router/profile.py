from fastapi import APIRouter,Depends

profile_router=APIRouter(tags=['profiles'],prefix='/profiles')


@profile_router.post('/new')
async def create_new_profile():
    pass 


@profile_router.patch('/update')
async def update_profile():
    pass 


@profile_router.delete('/{id}')
async def delete_profile(id:int):
    pass 

