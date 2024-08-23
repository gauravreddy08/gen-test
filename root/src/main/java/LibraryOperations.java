
public interface LibraryOperations<T> {
    void add(T item);
    void remove(T item);
    T search(String criteria);
}
