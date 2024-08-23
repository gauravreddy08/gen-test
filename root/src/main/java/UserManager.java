
import java.util.HashMap;
import java.util.Map;

public class UserManager implements LibraryOperations<User> {
    private final Map<String, User> users = new HashMap<>();

    @Override
    public void add(User user) {
        users.put(user.getId(), user);
    }

    @Override
    public void remove(User user) {
        users.remove(user.getId());
    }

    @Override
    public User search(String id) {
        return users.get(id);
    }
}
