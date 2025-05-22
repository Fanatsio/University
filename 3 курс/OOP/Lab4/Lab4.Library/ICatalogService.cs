namespace Lab4.Library
{
    internal interface ICatalogService
    {
        int AddProducts(Product Products);
        int AddBrands(Brand Brands);
        int AddCategories(Category categories);

        int UpdateProducts(int Id, string updatedProducts);
        int UpdateBrands(int Id, string updatedBrands);
        int UpdateCategories(int Id, string updatedCategories);

        Product ReadProducts(int ProductsId);
        Brand ReadBrands(int BrandsId);
        Category ReadCategories(int CategoriesId);

        int RemoveProducts(int ProductsName);
        int RemoveBrands(string nameBrands);
        int RemoveCategories(int nameCategories);
    }
}
