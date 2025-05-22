// Data/DatabaseContext.cs
using Npgsql;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CourseWork.Models;

namespace CourseWork.Data
{
    public class DatabaseContext
    {
        private readonly string _connectionString;

        public DatabaseContext(string connectionString)
        {
            _connectionString = connectionString;
        }

        #region Get Methods
        public async Task<ObservableCollection<NaturalPerson>> GetNaturalPersonsAsync()
        {
            var persons = new ObservableCollection<NaturalPerson>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM natural_person";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            persons.Add(new NaturalPerson
                            {
                                NaturalPersonId = reader.GetInt32(0),
                                NaturalPersonPassport = reader.GetInt32(1),
                                NaturalPersonName = reader.GetString(2),
                                NaturalPersonPhone = reader.GetString(3),
                                NaturalPersonEmail = reader.GetString(4),
                                NaturalPersonAddress = reader.GetString(5)
                            });
                        }
                    }
                }
            }
            return persons;
        }

        public async Task<ObservableCollection<LegalPerson>> GetLegalPersonsAsync()
        {
            var persons = new ObservableCollection<LegalPerson>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM legal_person";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            persons.Add(new LegalPerson
                            {
                                LegalPersonId = reader.GetInt32(0),
                                LegalPersonInn = reader.GetString(1),
                                LegalPersonName = reader.GetString(2),
                                LegalPersonPhone = reader.GetString(3),
                                LegalPersonEmail = reader.GetString(4),
                                LegalPersonAddress = reader.GetString(5)
                            });
                        }
                    }
                }
            }
            return persons;
        }

        public async Task<ObservableCollection<Provider>> GetProvidersAsync()
        {
            var providers = new ObservableCollection<Provider>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM provider";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            providers.Add(new Provider
                            {
                                ProviderId = reader.GetInt32(0),
                                ProviderInn = reader.GetString(1),
                                ProviderName = reader.GetString(2),
                                ProviderAddress = reader.GetString(3)
                            });
                        }
                    }
                }
            }
            return providers;
        }

        public async Task<ObservableCollection<Material>> GetMaterialsAsync()
        {
            var materials = new ObservableCollection<Material>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM material";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            materials.Add(new Material
                            {
                                MaterialId = reader.GetInt32(0),
                                MaterialColour = reader.GetString(1),
                                MaterialName = reader.GetString(2),
                                MaterialType = reader.GetString(3),
                                MaterialQuantity = reader.GetInt32(4),
                                ProviderInn = reader.GetString(5),
                                MaterialCost = reader.GetDecimal(6)
                            });
                        }
                    }
                }
            }
            return materials;
        }

        public async Task<ObservableCollection<Accessories>> GetAccessoriesAsync()
        {
            var accessories = new ObservableCollection<Accessories>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM accessories";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            accessories.Add(new Accessories
                            {
                                AccessoriesId = reader.GetInt32(0),
                                AccessoriesName = reader.GetString(1),
                                AccessoriesColour = reader.GetString(2),
                                AccessoriesType = reader.GetString(3),
                                AccessoriesQuantity = reader.GetInt32(4),
                                ProviderInn = reader.GetString(5),
                                AccessoriesCost = reader.GetDecimal(6)
                            });
                        }
                    }
                }
            }
            return accessories;
        }

        public async Task<ObservableCollection<Furniture>> GetFurnitureAsync()
        {
            var furniture = new ObservableCollection<Furniture>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM furniture";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            furniture.Add(new Furniture
                            {
                                FurnitureId = reader.GetInt32(0),
                                FurnitureColour = reader.GetString(1),
                                FurnitureArticle = reader.GetInt32(2),
                                IdMaterial = reader.GetInt32(3),
                                FurnitureType = reader.GetString(4),
                                FurnitureSize = reader.GetDecimal(5),
                                FurnitureName = reader.GetString(6),
                                IdAccessories = reader.GetInt32(7)
                            });
                        }
                    }
                }
            }
            return furniture;
        }

        public async Task<ObservableCollection<Order>> GetOrdersAsync()
        {
            var orders = new ObservableCollection<Order>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM orders";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            orders.Add(new Order
                            {
                                OrdersId = reader.GetInt32(0),
                                OrdersRegistrationDate = reader.GetDateTime(1),
                                OrdersTotalCost = reader.GetDecimal(2),
                                OrderNumber = reader.GetInt32(3),
                                CategoryCustomer = reader.GetString(4),
                                OrdersStatus = reader.GetString(5),
                                CustomerId = reader.GetInt32(6)
                            });
                        }
                    }
                }
            }
            return orders;
        }

        public async Task<ObservableCollection<Waybill>> GetWaybillsAsync()
        {
            var waybills = new ObservableCollection<Waybill>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                await conn.OpenAsync();
                string sql = "SELECT * FROM waybill";
                using (var cmd = new NpgsqlCommand(sql, conn))
                {
                    using (var reader = await cmd.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            waybills.Add(new Waybill
                            {
                                WaybillId = reader.GetInt32(0),
                                WaybillNumber = reader.GetInt32(1),
                                ArticleFurniture = reader.GetInt32(2),
                                FurnitureQuantity = reader.GetInt32(3),
                                OrdersNumber = reader.GetInt32(4)
                            });
                        }
                    }
                }
            }
            return waybills;
        }
        #endregion

        #region CRUD для NaturalPerson
        public async Task AddNaturalPersonAsync(NaturalPerson person)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO natural_person (natural_person_passport, natural_person_name, 
                                   natural_person_phone, natural_person_email, natural_person_address)
                                   VALUES (@passport, @name, @phone, @email, @address)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("passport", person.NaturalPersonPassport);
                        cmd.Parameters.AddWithValue("name", person.NaturalPersonName);
                        cmd.Parameters.AddWithValue("phone", person.NaturalPersonPhone);
                        cmd.Parameters.AddWithValue("email", person.NaturalPersonEmail);
                        cmd.Parameters.AddWithValue("address", person.NaturalPersonAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении физического лица: " + ex.Message);
            }
        }

        public async Task UpdateNaturalPersonAsync(NaturalPerson person)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE natural_person SET natural_person_passport = @passport, natural_person_name = @name, 
                                   natural_person_phone = @phone, natural_person_email = @email, natural_person_address = @address
                                   WHERE natural_person_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", person.NaturalPersonId);
                        cmd.Parameters.AddWithValue("passport", person.NaturalPersonPassport);
                        cmd.Parameters.AddWithValue("name", person.NaturalPersonName);
                        cmd.Parameters.AddWithValue("phone", person.NaturalPersonPhone);
                        cmd.Parameters.AddWithValue("email", person.NaturalPersonEmail);
                        cmd.Parameters.AddWithValue("address", person.NaturalPersonAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении физического лица: " + ex.Message);
            }
        }

        public async Task DeleteNaturalPersonAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM natural_person WHERE natural_person_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении физического лица: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для LegalPerson
        public async Task AddLegalPersonAsync(LegalPerson person)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO legal_person (legal_person_inn, legal_person_name, 
                                   legal_person_phone, legal_person_email, legal_person_address)
                                   VALUES (@inn, @name, @phone, @email, @address)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("inn", person.LegalPersonInn);
                        cmd.Parameters.AddWithValue("name", person.LegalPersonName);
                        cmd.Parameters.AddWithValue("phone", person.LegalPersonPhone);
                        cmd.Parameters.AddWithValue("email", person.LegalPersonEmail);
                        cmd.Parameters.AddWithValue("address", person.LegalPersonAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении юридического лица: " + ex.Message);
            }
        }

        public async Task UpdateLegalPersonAsync(LegalPerson person)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE legal_person SET legal_person_inn = @inn, legal_person_name = @name, 
                                   legal_person_phone = @phone, legal_person_email = @email, legal_person_address = @address
                                   WHERE legal_person_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", person.LegalPersonId);
                        cmd.Parameters.AddWithValue("inn", person.LegalPersonInn);
                        cmd.Parameters.AddWithValue("name", person.LegalPersonName);
                        cmd.Parameters.AddWithValue("phone", person.LegalPersonPhone);
                        cmd.Parameters.AddWithValue("email", person.LegalPersonEmail);
                        cmd.Parameters.AddWithValue("address", person.LegalPersonAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении юридического лица: " + ex.Message);
            }
        }

        public async Task DeleteLegalPersonAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM legal_person WHERE legal_person_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении юридического лица: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Provider
        public async Task AddProviderAsync(Provider provider)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO provider (provider_inn, provider_name, provider_address)
                                   VALUES (@inn, @name, @address)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("inn", provider.ProviderInn);
                        cmd.Parameters.AddWithValue("name", provider.ProviderName);
                        cmd.Parameters.AddWithValue("address", provider.ProviderAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении поставщика: " + ex.Message);
            }
        }

        public async Task UpdateProviderAsync(Provider provider)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE provider SET provider_inn = @inn, provider_name = @name, 
                                   provider_address = @address WHERE provider_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", provider.ProviderId);
                        cmd.Parameters.AddWithValue("inn", provider.ProviderInn);
                        cmd.Parameters.AddWithValue("name", provider.ProviderName);
                        cmd.Parameters.AddWithValue("address", provider.ProviderAddress);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении поставщика: " + ex.Message);
            }
        }

        public async Task DeleteProviderAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM provider WHERE provider_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении поставщика: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Material
        public async Task AddMaterialAsync(Material material)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO material (material_colour, material_name, material_type, 
                                   material_quantity, provider_inn, material_cost)
                                   VALUES (@colour, @name, @type, @quantity, @providerInn, @cost)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("colour", material.MaterialColour);
                        cmd.Parameters.AddWithValue("name", material.MaterialName);
                        cmd.Parameters.AddWithValue("type", material.MaterialType);
                        cmd.Parameters.AddWithValue("quantity", material.MaterialQuantity);
                        cmd.Parameters.AddWithValue("providerInn", material.ProviderInn);
                        cmd.Parameters.AddWithValue("cost", material.MaterialCost);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении материала: " + ex.Message);
            }
        }

        public async Task UpdateMaterialAsync(Material material)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE material SET material_colour = @colour, material_name = @name, 
                                   material_type = @type, material_quantity = @quantity, provider_inn = @providerInn, 
                                   material_cost = @cost WHERE material_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", material.MaterialId);
                        cmd.Parameters.AddWithValue("colour", material.MaterialColour);
                        cmd.Parameters.AddWithValue("name", material.MaterialName);
                        cmd.Parameters.AddWithValue("type", material.MaterialType);
                        cmd.Parameters.AddWithValue("quantity", material.MaterialQuantity);
                        cmd.Parameters.AddWithValue("providerInn", material.ProviderInn);
                        cmd.Parameters.AddWithValue("cost", material.MaterialCost);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении материала: " + ex.Message);
            }
        }

        public async Task DeleteMaterialAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM material WHERE material_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении материала: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Accessories
        public async Task AddAccessoriesAsync(Accessories accessories)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO accessories (accessories_name, accessories_colour, accessories_type, 
                                   accessories_quantity, provider_inn, accessories_cost)
                                   VALUES (@name, @colour, @type, @quantity, @providerInn, @cost)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("name", accessories.AccessoriesName);
                        cmd.Parameters.AddWithValue("colour", accessories.AccessoriesColour);
                        cmd.Parameters.AddWithValue("type", accessories.AccessoriesType);
                        cmd.Parameters.AddWithValue("quantity", accessories.AccessoriesQuantity);
                        cmd.Parameters.AddWithValue("providerInn", accessories.ProviderInn);
                        cmd.Parameters.AddWithValue("cost", accessories.AccessoriesCost);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении фурнитуры: " + ex.Message);
            }
        }

        public async Task UpdateAccessoriesAsync(Accessories accessories)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE accessories SET accessories_name = @name, accessories_colour = @colour, 
                                   accessories_type = @type, accessories_quantity = @quantity, provider_inn = @providerInn, 
                                   accessories_cost = @cost WHERE accessories_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", accessories.AccessoriesId);
                        cmd.Parameters.AddWithValue("name", accessories.AccessoriesName);
                        cmd.Parameters.AddWithValue("colour", accessories.AccessoriesColour);
                        cmd.Parameters.AddWithValue("type", accessories.AccessoriesType);
                        cmd.Parameters.AddWithValue("quantity", accessories.AccessoriesQuantity);
                        cmd.Parameters.AddWithValue("providerInn", accessories.ProviderInn);
                        cmd.Parameters.AddWithValue("cost", accessories.AccessoriesCost);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении фурнитуры: " + ex.Message);
            }
        }

        public async Task DeleteAccessoriesAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM accessories WHERE accessories_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении фурнитуры: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Furniture
        public async Task AddFurnitureAsync(Furniture furniture)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO furniture (furniture_colour, furniture_article, id_material, 
                                   furniture_type, furniture_size, furniture_name, id_accessories)
                                   VALUES (@colour, @article, @material, @type, @size, @name, @accessories)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("colour", furniture.FurnitureColour);
                        cmd.Parameters.AddWithValue("article", furniture.FurnitureArticle);
                        cmd.Parameters.AddWithValue("material", furniture.IdMaterial);
                        cmd.Parameters.AddWithValue("type", furniture.FurnitureType);
                        cmd.Parameters.AddWithValue("size", furniture.FurnitureSize);
                        cmd.Parameters.AddWithValue("name", furniture.FurnitureName);
                        cmd.Parameters.AddWithValue("accessories", furniture.IdAccessories);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении мебели: " + ex.Message);
            }
        }

        public async Task UpdateFurnitureAsync(Furniture furniture)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE furniture SET furniture_colour = @colour, furniture_article = @article, 
                                   id_material = @material, furniture_type = @type, furniture_size = @size, 
                                   furniture_name = @name, id_accessories = @accessories WHERE furniture_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", furniture.FurnitureId);
                        cmd.Parameters.AddWithValue("colour", furniture.FurnitureColour);
                        cmd.Parameters.AddWithValue("article", furniture.FurnitureArticle);
                        cmd.Parameters.AddWithValue("material", furniture.IdMaterial);
                        cmd.Parameters.AddWithValue("type", furniture.FurnitureType);
                        cmd.Parameters.AddWithValue("size", furniture.FurnitureSize);
                        cmd.Parameters.AddWithValue("name", furniture.FurnitureName);
                        cmd.Parameters.AddWithValue("accessories", furniture.IdAccessories);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении мебели: " + ex.Message);
            }
        }

        public async Task DeleteFurnitureAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM furniture WHERE furniture_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении мебели: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Order
        public async Task AddOrderAsync(Order order)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO orders (orders_registration_date, orders_total_cost, order_number, 
                                   category_customer, orders_status, customer_id)
                                   VALUES (@date, @cost, @number, @category, @status, @customer)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("date", order.OrdersRegistrationDate);
                        cmd.Parameters.AddWithValue("cost", order.OrdersTotalCost);
                        cmd.Parameters.AddWithValue("number", order.OrderNumber);
                        cmd.Parameters.AddWithValue("category", order.CategoryCustomer);
                        cmd.Parameters.AddWithValue("status", order.OrdersStatus);
                        cmd.Parameters.AddWithValue("customer", order.CustomerId);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении заказа: " + ex.Message);
            }
        }

        public async Task UpdateOrderAsync(Order order)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE orders SET orders_registration_date = @date, orders_total_cost = @cost, 
                                   order_number = @number, category_customer = @category, orders_status = @status, 
                                   customer_id = @customer WHERE orders_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", order.OrdersId);
                        cmd.Parameters.AddWithValue("date", order.OrdersRegistrationDate);
                        cmd.Parameters.AddWithValue("cost", order.OrdersTotalCost);
                        cmd.Parameters.AddWithValue("number", order.OrderNumber);
                        cmd.Parameters.AddWithValue("category", order.CategoryCustomer);
                        cmd.Parameters.AddWithValue("status", order.OrdersStatus);
                        cmd.Parameters.AddWithValue("customer", order.CustomerId);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении заказа: " + ex.Message);
            }
        }

        public async Task DeleteOrderAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM orders WHERE orders_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении заказа: " + ex.Message);
            }
        }
        #endregion

        #region CRUD для Waybill
        public async Task AddWaybillAsync(Waybill waybill)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"INSERT INTO waybill (waybill_number, article_furniture, furniture_quantity, orders_number)
                                   VALUES (@number, @article, @quantity, @order)";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("number", waybill.WaybillNumber);
                        cmd.Parameters.AddWithValue("article", waybill.ArticleFurniture);
                        cmd.Parameters.AddWithValue("quantity", waybill.FurnitureQuantity);
                        cmd.Parameters.AddWithValue("order", waybill.OrdersNumber);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при добавлении накладной: " + ex.Message);
            }
        }

        public async Task UpdateWaybillAsync(Waybill waybill)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = @"UPDATE waybill SET waybill_number = @number, article_furniture = @article, 
                                   furniture_quantity = @quantity, orders_number = @order WHERE waybill_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", waybill.WaybillId);
                        cmd.Parameters.AddWithValue("number", waybill.WaybillNumber);
                        cmd.Parameters.AddWithValue("article", waybill.ArticleFurniture);
                        cmd.Parameters.AddWithValue("quantity", waybill.FurnitureQuantity);
                        cmd.Parameters.AddWithValue("order", waybill.OrdersNumber);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при обновлении накладной: " + ex.Message);
            }
        }

        public async Task DeleteWaybillAsync(int id)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "DELETE FROM waybill WHERE waybill_id = @id";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("id", id);
                        await cmd.ExecuteNonQueryAsync();
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при удалении накладной: " + ex.Message);
            }
        }
        #endregion

        // Новый метод для авторизации
        public async Task<User> AuthenticateUserAsync(string username, string password)
        {
            try
            {
                using (var conn = new NpgsqlConnection(_connectionString))
                {
                    await conn.OpenAsync();
                    string sql = "SELECT * FROM users WHERE username = @username AND password = @password";
                    using (var cmd = new NpgsqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("username", username);
                        cmd.Parameters.AddWithValue("password", password);
                        using (var reader = await cmd.ExecuteReaderAsync())
                        {
                            if (await reader.ReadAsync())
                            {
                                return new User
                                {
                                    UserId = reader.GetInt32(0),
                                    Username = reader.GetString(1),
                                    Password = reader.GetString(2)
                                };
                            }
                        }
                    }
                }
                return null; // Пользователь не найден
            }
            catch (Exception ex)
            {
                throw new Exception("Ошибка при авторизации: " + ex.Message);
            }
        }
    }
}