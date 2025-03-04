// tr101290_analyzer.h
#ifndef TR101290_ANALYZER_H
#define TR101290_ANALYZER_H

#include <stdio.h>
#include <stdlib.h>

#define TS_PACKET_SIZE 188

// 错误统计结构体
typedef struct {
    int sync_byte_errors;       // 同步字节错误
    int pat_errors;             // PAT表错误
    int continuity_count_errors; // 连续计数错误
    int pmt_errors;             // PMT表错误
    int pcr_errors;             // PCR错误
    int nit_errors;             // NIT表错误
    int si_repetition_errors;   // SI表重复错误
} TR101290ErrorStats;

// 初始化错误统计
void init_error_stats(TR101290ErrorStats* stats);

// 分析TS文件并统计错误
void analyze_ts_file(const char* filename, TR101290ErrorStats* stats);

// 生成错误统计报表
void generate_error_report(const TR101290ErrorStats* stats);

#endif // TR101290_ANALYZER_H