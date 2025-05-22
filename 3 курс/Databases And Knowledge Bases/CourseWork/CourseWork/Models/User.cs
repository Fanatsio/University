// Models/User.cs
namespace CourseWork.Models
{
    public class User
    {
        public int UserId { get; set; }
        public string Username { get; set; }
        public string Password { get; set; } // В реальном проекте используйте хеширование!
    }
}