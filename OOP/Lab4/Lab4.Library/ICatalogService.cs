namespace Lab4.Library
{
    internal interface ICatalogService
    {
        int AddProducts(Products Products);
        int AddBrands(Brands Brands);
        int AddCategories(Categories categories);

        int UpdateProducts(int Id, string updatedProducts);
        int UpdateBrands(int Id, string updatedBrands);
        int UpdateCategories(int Id, string updatedCategories);

        Products ReadProducts(int ProductsId);
        Brands ReadBrands(int BrandsId);
        Categories ReadCategories(int CategoriesId);

        int RemoveProducts(int ProductsName);
        int RemoveBrands(string nameBrands);
        int RemoveCategories(int nameCategories);
    }
}
