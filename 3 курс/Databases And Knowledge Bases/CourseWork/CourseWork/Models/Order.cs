namespace CourseWork.Models
{
    public class Order
    {
        public int OrdersId { get; set; }
        public DateTime OrdersRegistrationDate { get; set; }
        public decimal OrdersTotalCost { get; set; }
        public int OrderNumber { get; set; }
        public string CategoryCustomer { get; set; }
        public string OrdersStatus { get; set; }
        public int CustomerId { get; set; }
    }
}