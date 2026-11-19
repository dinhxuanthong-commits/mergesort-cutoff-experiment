package algorithms;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Runner thực nghiệm siêu chi tiết:
 * Khảo sát toàn bộ các giá trị nguyên từ 1 đến 50 (bước 1),
 * cùng dải mở rộng tới 100 (tổng cộng 66 giá trị CUTOFF).
 */
public class ExperimentRunner {

    public enum DataType {
        RANDOM, SORTED, REVERSED, NEARLY_SORTED, MANY_DUPLICATES
    }

    // 66 giá trị CUTOFF: đầy đủ từng số nguyên từ 1 đến 50, sau đó mở rộng đến 100
    public static final int[] CUTOFFS = {
        1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
        52, 54, 56, 58, 60, 62, 64, 66, 68, 70,
        75, 80, 85, 90, 95, 100
    };

    public static final int[] SIZES = {
        500, 1_000, 5_000, 10_000, 50_000, 100_000
    };

    public static final int TRIALS = 15;
    public static final int WARMUP_RUNS = 3;

    public static void main(String[] args) {
        boolean isSmokeTest = false;
        long seed = 2024L;
        for (String arg : args) {
            if ("--smoke-test".equals(arg)) isSmokeTest = true;
            else if (arg.startsWith("--seed=")) {
                try {
                    seed = Long.parseLong(arg.substring(7));
                } catch (NumberFormatException ignored) {}
            }
        }

        int[] activeCutoffs = isSmokeTest ? new int[]{1, 5, 7, 10, 15, 20, 23, 25, 30} : CUTOFFS;
        int[] activeSizes = isSmokeTest ? new int[]{500, 1_000} : SIZES;
        int activeTrials = isSmokeTest ? 3 : TRIALS;
        int activeWarmup = isSmokeTest ? 1 : WARMUP_RUNS;

        System.out.println("==================================================================");
        if (isSmokeTest) {
            System.out.println("  CHẾ ĐỘ KIỂM THỬ NHANH (SMOKE-TEST EXPERIMENT RUNNER)");
        } else {
            System.out.println("  THỰC NGHIỆM SIÊU DÀY ĐẶC: 66 GIÁ TRỊ CUTOFF (TỪ 1 ĐẾN 100)");
            System.out.println("  Khảo sát từng số nguyên 1..50 để xác định chính xác đỉnh tối ưu");
        }
        System.out.println("==================================================================");
        System.out.printf("  Số mốc CUTOFF khảo sát: %d%n", activeCutoffs.length);
        System.out.printf("  Số lần lặp (Trials): %d%n", activeTrials);
        System.out.printf("  JVM: %s %s%n", System.getProperty("java.vendor"), System.getProperty("java.version"));
        System.out.printf("  OS:  %s (%s)%n%n", System.getProperty("os.name"), System.getProperty("os.arch"));

        Random rng = new Random(seed);
        List<String> csvRows = new ArrayList<>();
        csvRows.add("cutoff,n,dataType,trials,medianMs,meanMs,minMs,maxMs");

        Map<String, Double> baselineMap = new HashMap<>();
        Map<Integer, List<Double>> speedupPerCutoff = new TreeMap<>();

        for (DataType type : DataType.values()) {
            System.out.printf("%n>>> Đang đo dữ liệu: %-16s%n", type);

            for (int n : activeSizes) {
                Integer[] original = generateData(n, type, rng);
                System.out.printf("  N = %6d | ", n);

                for (int cutoff : activeCutoffs) {
                    // Warm-up JIT
                    for (int w = 0; w < activeWarmup; w++) {
                        Integer[] copy = original.clone();
                        Mergesort.sort(copy, cutoff);
                    }

                    // Đo thời gian các lần lặp
                    double[] times = new double[activeTrials];
                    for (int t = 0; t < activeTrials; t++) {
                        Integer[] copy = original.clone();
                        long start = System.nanoTime();
                        Mergesort.sort(copy, cutoff);
                        times[t] = (System.nanoTime() - start) / 1_000_000.0;
                    }

                    Arrays.sort(times);
                    double median = (activeTrials % 2 == 0)
                            ? (times[activeTrials / 2 - 1] + times[activeTrials / 2]) / 2.0
                            : times[activeTrials / 2];

                    double sum = 0;
                    for (double val : times) sum += val;
                    double mean = sum / activeTrials;

                    csvRows.add(String.format(Locale.US, "%d,%d,%s,%d,%.6f,%.6f,%.6f,%.6f",
                            cutoff, n, type.name(), activeTrials, median, mean, times[0], times[activeTrials - 1]));

                    if (cutoff == 1) {
                        baselineMap.put(n + "|" + type.name(), median);
                        System.out.printf("[Base: %.3fms] ", median);
                    } else {
                        double base = baselineMap.getOrDefault(n + "|" + type.name(), median);
                        double speedup = (base > 0 && median > 0) ? base / median : 1.0;
                        speedupPerCutoff.computeIfAbsent(cutoff, k -> new ArrayList<>()).add(speedup);
                    }
                }
                System.out.println();
            }
        }

        // Xuất file CSV
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        Path resultsDir = Paths.get("results");
        String prefix = isSmokeTest ? "experiment_smoke_test_" : "experiment_dense_66cutoffs_";
        Path csvPath = resultsDir.resolve(prefix + timestamp + ".csv");
        try {
            Files.createDirectories(resultsDir);
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvPath.toFile()))) {
                for (String row : csvRows) {
                    writer.write(row);
                    writer.newLine();
                }
            }
            System.out.printf("%n[OK] Kết quả đã ghi vào: %s (%d dòng)%n", csvPath, csvRows.size());
        } catch (IOException e) {
            System.err.println("Lỗi ghi CSV: " + e.getMessage());
        }

        // In bảng tổng kết
        printSummary(speedupPerCutoff);
    }

    private static void printSummary(Map<Integer, List<Double>> speedupMap) {
        System.out.println("\n+-------------------------------------------------------------+");
        System.out.println("|    BẢNG TỔNG KẾT TỈ SỐ TĂNG TỐC CHI TIẾT (CUTOFF 1 -> 100)  |");
        System.out.println("+-------------------------------------------------------------+");
        System.out.printf("%-8s %-15s %-25s%n", "CUTOFF", "Speedup TB", "Ghi chú");
        System.out.println("-------------------------------------------------------------");

        int bestCutoff = 1;
        double bestAvg = 0.0;

        for (Map.Entry<Integer, List<Double>> entry : speedupMap.entrySet()) {
            int cutoff = entry.getKey();
            List<Double> ratios = entry.getValue();
            double avg = ratios.stream().mapToDouble(Double::doubleValue).average().orElse(1.0);

            String note = "";
            if (cutoff == 7) note = "<-- Giáo trình cũ";
            else if (cutoff == 10) note = "<-- Giáo trình mới";

            System.out.printf(Locale.US, "%-8d %-15.4f %-25s%n", cutoff, avg, note);

            if (avg > bestAvg) {
                bestAvg = avg;
                bestCutoff = cutoff;
            }
        }

        System.out.println("-------------------------------------------------------------");
        System.out.printf(Locale.US, ">>> ĐỈNH TỐI ƯU TOÀN CỤC: CUTOFF = %d (Tăng tốc: %.2f%% so với Mergesort thuần)%n%n",
                bestCutoff, (bestAvg - 1.0) * 100);
    }

    private static Integer[] generateData(int n, DataType type, Random rng) {
        Integer[] a = new Integer[n];
        switch (type) {
            case RANDOM:
                for (int i = 0; i < n; i++) a[i] = rng.nextInt(n * 10);
                break;
            case SORTED:
                for (int i = 0; i < n; i++) a[i] = i;
                break;
            case REVERSED:
                for (int i = 0; i < n; i++) a[i] = n - i;
                break;
            case NEARLY_SORTED:
                for (int i = 0; i < n; i++) a[i] = i;
                int swaps = Math.max(1, n / 20);
                for (int s = 0; s < swaps; s++) {
                    int i = rng.nextInt(n);
                    int j = rng.nextInt(n);
                    Integer tmp = a[i]; a[i] = a[j]; a[j] = tmp;
                }
                break;
            case MANY_DUPLICATES:
                int range = (int) Math.sqrt(n) + 1;
                for (int i = 0; i < n; i++) a[i] = rng.nextInt(range);
                break;
        }
        return a;
    }
}
