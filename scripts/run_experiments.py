#!/usr/bin/env python3
"""
run_experiments.py
Chạy thực nghiệm đo lường hiệu năng bằng cách gọi fat JAR đã đóng gói
hoặc chạy trực tiếp từ compiled bytecode trong target/classes.
Sử dụng cờ JVM cố định: -Xms2g -Xmx2g -XX:+UseG1GC để triệt tiêu biến động Heap & GC.
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def find_java_binary() -> str:
    # 1. Ưu tiên trực tiếp JDK thực tế để tránh Oracle javapath wrapper bị treo trên Windows sandbox
    jdk_dirs = list(Path(r"C:\Program Files\Java").glob("jdk*"))
    if jdk_dirs:
        latest_jdk = sorted(jdk_dirs)[-1]
        java_exe = latest_jdk / "bin" / "java.exe"
        if java_exe.exists():
            return str(java_exe)

    # 2. Kiểm tra JAVA_HOME
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        java_exe = Path(java_home) / "bin" / "java.exe"
        if java_exe.exists():
            return str(java_exe)

    # 3. Kiểm tra java trong PATH (nếu không phải Oracle wrapper)
    java_in_path = shutil.which("java")
    if java_in_path and "Common Files" not in java_in_path:
        return java_in_path

    return "java"


def find_runner_target():
    target_dir = Path("target")
    # Ưu tiên Fat JAR nếu có
    jars = list(target_dir.glob("mergesort-cutoff-experiment-*.jar"))
    jars = [j for j in jars if not j.name.startswith("original-")]
    if jars:
        return "jar", sorted(jars)[-1]

    # Kiểm tra target/classes
    classes_dir = target_dir / "classes"
    runner_class = classes_dir / "algorithms" / "ExperimentRunner.class"
    if runner_class.exists():
        return "classes", classes_dir

    print("[ERROR] Không tìm thấy JAR hoặc compiled classes trong thư mục 'target/'.")
    print("Vui lòng biên dịch trước bằng: javac -d target/classes src/main/java/algorithms/*.java")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Chạy thực nghiệm MergeSort CUTOFF trên máy thật")
    parser.add_argument("--smoke-test", action="store_true", help="Chạy chế độ kiểm thử nhanh")
    parser.add_argument("--seed", type=int, default=2024, help="Random seed")
    parser.add_argument("--jvm-mem", type=str, default="2g", help="Dung lượng bộ nhớ JVM cố định (ví dụ: 1g, 2g)")
    args = parser.parse_args()

    java_bin = find_java_binary()
    target_type, target_path = find_runner_target()

    # Cờ JVM tối ưu cho benchmark khoa học
    jvm_args = [
        java_bin,
        f"-Xms{args.jvm_mem}",
        f"-Xmx{args.jvm_mem}",
        "-XX:+UseG1GC",
    ]

    if target_type == "jar":
        print(f"[INFO] Sử dụng JAR: {target_path}")
        jvm_args.extend(["-jar", str(target_path)])
    else:
        print(f"[INFO] Sử dụng Classpath: {target_path}")
        jvm_args.extend(["-cp", str(target_path), "algorithms.ExperimentRunner"])

    if args.smoke_test:
        jvm_args.append("--smoke-test")
    if args.seed:
        jvm_args.append(f"--seed={args.seed}")

    cmd_str = " ".join(jvm_args)
    print(f"[EXEC] Chạy lệnh: {cmd_str}\n")

    result = subprocess.run(jvm_args)
    if result.returncode != 0:
        print(f"\n[ERROR] Quá trình thực nghiệm kết thúc với mã lỗi: {result.returncode}")
        sys.exit(result.returncode)

    print("\n[SUCCESS] Thực nghiệm hoàn tất thành công. Dữ liệu CSV đã lưu vào thư mục 'results/'.")


if __name__ == "__main__":
    main()
