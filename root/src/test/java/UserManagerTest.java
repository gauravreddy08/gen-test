import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UserManagerTest {
    private UserManager userManager;
    private User user1;
    private User user2;

    @BeforeEach
    public void setUp() {
        userManager = new UserManager();
        user1 = new User("Alice", "1");
        user2 = new User("Bob", "2");
    }

    @Test
    public void testAddUser() {
        userManager.add(user1);
        assertEquals(user1, userManager.search("1"));
    }

    @Test
    public void testRemoveUser() {
        userManager.add(user1);
        userManager.remove(user1);
        assertNull(userManager.search("1"));
    }

    @Test
    public void testSearchUser() {
        userManager.add(user1);
        userManager.add(user2);
        assertEquals(user2, userManager.search("2"));
        assertEquals(user1, userManager.search("1"));
    }

    @Test
    public void testSearchNonExistentUser() {
        assertNull(userManager.search("3"));
    }

    @Test
    public void testAddDuplicateUser() {
        userManager.add(user1);
        User duplicateUser = new User("Alice Duplicate", "1");
        userManager.add(duplicateUser);
        assertEquals(duplicateUser, userManager.search("1"));
    }
}
