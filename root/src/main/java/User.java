
import java.util.ArrayList;
import java.util.List;

public class User {
    private String name;
    private String id;
    private List<BorrowRecord> borrowRecords;

    public User(String name, String id) {
        this.name = name;
        this.id = id;
        this.borrowRecords = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public List<BorrowRecord> getBorrowRecords() {
        return borrowRecords;
    }

    public void addBorrowRecord(BorrowRecord record) {
        borrowRecords.add(record);
    }
}
