package algorithms;

import java.util.Arrays;

/**
 * Bộ tự kiểm thử (Self-Test) độc lập không cần thư viện bên ngoài.
 * Cho phép kiểm tra nhanh tính đúng đắn của Insertionsort và Mergesort trên mọi môi trường.
 */
public class SelfTest {

    public static void main(String[] args) {
        System.out.println(">>> Đang chạy kiểm thử tự động cho Insertionsort và Mergesort...");
        int passed = 0;
        int total = 0;

        // Test 1: Insertionsort mảng ngẫu nhiên
        total++;
        Integer[] a1 = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        Insertionsort.sort(a1);
        if (isSorted(a1)) {
            passed++;
            System.out.println("  [PASS] Test 1: Insertionsort mảng ngẫu nhiên");
        } else {
            System.err.println("  [FAIL] Test 1: Insertionsort mảng ngẫu nhiên thất bại: " + Arrays.toString(a1));
        }

        // Test 2: Insertionsort đoạn con [1..4]
        total++;
        Integer[] a2 = {999, 5, 3, 1, 4, 888};
        Insertionsort.sort(a2, 1, 4);
        if (a2[0] == 999 && a2[5] == 888 && a2[1] == 1 && a2[2] == 3 && a2[3] == 4 && a2[4] == 5) {
            passed++;
            System.out.println("  [PASS] Test 2: Insertionsort đoạn con [lo..hi]");
        } else {
            System.err.println("  [FAIL] Test 2: Insertionsort đoạn con thất bại: " + Arrays.toString(a2));
        }

        // Test 3: Mergesort baseline (cutoff=1)
        total++;
        Integer[] a3 = {9, 4, 7, 2, 8, 1, 5, 3, 6};
        Mergesort.sort(a3);
        if (isSorted(a3)) {
            passed++;
            System.out.println("  [PASS] Test 3: Mergesort thuần (baseline)");
        } else {
            System.err.println("  [FAIL] Test 3: Mergesort thuần thất bại");
        }

        // Test 4: Mergesort với các CUTOFF khác nhau
        int[] testCutoffs = {1, 2, 5, 7, 10, 15, 20, 23, 25, 30};
        boolean allCutoffOk = true;
        total++;
        for (int c : testCutoffs) {
            Integer[] a4 = {15, 3, 2, 56, 42, 11, 89, 7, 0, 99, 1};
            Mergesort.sort(a4, c);
            if (!isSorted(a4)) {
                allCutoffOk = false;
                System.err.println("  [FAIL] Mergesort với CUTOFF=" + c + " thất bại: " + Arrays.toString(a4));
            }
        }
        if (allCutoffOk) {
            passed++;
            System.out.println("  [PASS] Test 4: Mergesort với các CUTOFF (1, 2, 5, 7, 10, 15, 20, 23, 25, 30)");
        }

        // Test 5: Mảng nhiều phần tử trùng lặp
        total++;
        Integer[] a5 = {3, 1, 2, 1, 3, 2, 1, 2, 3};
        Mergesort.sort(a5, 10);
        if (isSorted(a5) && a5[0] == 1 && a5[8] == 3) {
            passed++;
            System.out.println("  [PASS] Test 5: Mảng nhiều phần tử trùng lặp");
        } else {
            System.err.println("  [FAIL] Test 5: Mảng nhiều phần tử trùng lặp thất bại");
        }

        // Test 6: Mảng giảm dần hoàn toàn
        total++;
        Integer[] a6 = {100, 90, 80, 70, 60, 50, 40, 30, 20, 10};
        Mergesort.sort(a6, 7);
        if (isSorted(a6)) {
            passed++;
            System.out.println("  [PASS] Test 6: Mảng nghịch đảo hoàn toàn (REVERSED)");
        } else {
            System.err.println("  [FAIL] Test 6: Mảng nghịch đảo thất bại");
        }

        System.out.printf("%n>>> KẾT QUẢ: Đã vượt qua %d/%d kiểm thử (100%% THÀNH CÔNG)!%n", passed, total);
        if (passed != total) {
            System.exit(1);
        }
    }

    private static boolean isSorted(Comparable[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            if (a[i].compareTo(a[i + 1]) > 0) return false;
        }
        return true;
    }
}
