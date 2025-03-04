// tr101290_analyzer.c
#include "tr101290_analyzer.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// 初始化错误统计
void init_error_stats(TR101290ErrorStats* stats) {
    stats->sync_byte_errors = 0;
    stats->pat_errors = 0;
    stats->continuity_count_errors = 0;
    stats->pmt_errors = 0;
    stats->pcr_errors = 0;
    stats->nit_errors = 0;
    stats->si_repetition_errors = 0;
}

// 检查同步字节错误
void check_sync_byte(const unsigned char* packet, TR101290ErrorStats* stats) {
    if (packet[0] != 0x47) {
        stats->sync_byte_errors++;
    }
}

// 检查PAT表错误（示例逻辑，需根据实际PAT表解析实现）
void check_pat(const unsigned char* packet, TR101290ErrorStats* stats) {
    // 假设PID为0x0000的包是PAT表
    if (((packet[1] & 0x1F) << 8 | packet[2]) == 0x0000) {
        // 检查PAT表是否有效
        if (packet[5] != 0x00) {  // 假设PAT表的table_id为0x00
            stats->pat_errors++;
        }
    }
}

// 检查连续计数错误
void check_continuity_count(const unsigned char* packet, int* last_continuity_count, int* last_pid, TR101290ErrorStats* stats) {
    int current_pid = ((packet[1] & 0x1F) << 8) | packet[2];
    int adaptation_field_control = (packet[3] >> 4) & 0x03;
    int current_continuity_count = packet[3] & 0x0F;

    // 只检查相同PID的包
    if (*last_pid == current_pid) {
        // 如果adaptation_field_control为0b10或0b00，表示没有有效负载，continuity_counter可能不递增
        if (adaptation_field_control != 0b10 && adaptation_field_control != 0b00) {
            if (*last_continuity_count != -1 && (current_continuity_count != (*last_continuity_count + 1) % 16)) {
                stats->continuity_count_errors++;
            }
            *last_continuity_count = current_continuity_count;
        }
    } else {
        // 更新PID并重置continuity_count
        *last_pid = current_pid;
        *last_continuity_count = current_continuity_count;
    }
}

// 分析TS文件并统计错误
void analyze_ts_file(const char* filename, TR101290ErrorStats* stats) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        perror("Failed to open file");
        exit(EXIT_FAILURE);
    }

    unsigned char packet[TS_PACKET_SIZE];
    int last_continuity_count = -1;
    int last_pid = -1;

    while (fread(packet, 1, TS_PACKET_SIZE, file) == TS_PACKET_SIZE) {
        // 检查一级错误
        check_sync_byte(packet, stats);
        check_pat(packet, stats);
        check_continuity_count(packet, &last_continuity_count, &last_pid, stats);

        // 检查二级和三级错误（需根据实际需求实现）
        // check_pmt(packet, stats);
        // check_pcr(packet, stats);
        // check_nit(packet, stats);
        // check_si_repetition(packet, stats);
    }

    fclose(file);
}

// 生成错误统计报表
void generate_error_report(const TR101290ErrorStats* stats) {
    printf("===== TR 101 290 Error Report =====\n");
    printf("Priority 1 Errors:\n");
    printf("  Sync Byte Errors: %d\n", stats->sync_byte_errors);
    printf("  PAT Errors: %d\n", stats->pat_errors);
    printf("  Continuity Count Errors: %d\n", stats->continuity_count_errors);
    printf("Priority 2 Errors:\n");
    printf("  PMT Errors: %d\n", stats->pmt_errors);
    printf("  PCR Errors: %d\n", stats->pcr_errors);
    printf("Priority 3 Errors:\n");
    printf("  NIT Errors: %d\n", stats->nit_errors);
    printf("  SI Repetition Errors: %d\n", stats->si_repetition_errors);
    printf("===================================\n");
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <ts_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    TR101290ErrorStats stats;
    init_error_stats(&stats);

    analyze_ts_file(argv[1], &stats);
    generate_error_report(&stats);

    return EXIT_SUCCESS;
}