import { FormEvent, useEffect, useState } from "react";

import { getReports, type Report, updateReport } from "../api";

type AdminReportsProps = {
  onError: (message: string) => void;
};

export function AdminReports({ onError }: AdminReportsProps) {
  const [reports, setReports] = useState<Report[]>([]);
  const [query, setQuery] = useState("");

  async function loadReports(nextQuery = query) {
    try {
      const items = await getReports(nextQuery);
      setReports(items);
      onError("");
    } catch (reason) {
      onError(reason instanceof Error ? reason.message : "신고 목록을 불러오지 못했습니다.");
    }
  }

  useEffect(() => {
    void loadReports("");
  }, []);

  async function handleDecision(reportId: number, status: "ACCEPTED" | "REJECTED") {
    try {
      await updateReport(reportId, status);
      setReports((current) => current.filter((report) => report.id !== reportId));
      onError("");
    } catch (reason) {
      onError(reason instanceof Error ? reason.message : "신고를 처리하지 못했습니다.");
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void loadReports(query);
  }

  return (
    <div className="report-panel">
      <div className="panel-header">
        <h2>신고 관리</h2>
      </div>
      <form className="inline-form" onSubmit={handleSubmit}>
        <label className="field grow">
          <span>검색</span>
          <input
            aria-label="신고 검색"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="사유 키워드"
          />
        </label>
        <button type="submit">검색</button>
      </form>
      {reports.length === 0 ? (
        <p className="empty-text">열린 신고가 없습니다.</p>
      ) : (
        <ul className="feed-list">
          {reports.map((report) => (
            <li key={report.id} className="feed-card">
              <div className="feed-meta">
                <strong>게시글 #{report.post_id}</strong>
                <span>{new Date(report.created_at).toLocaleString("ko-KR")}</span>
              </div>
              <p>{report.reason}</p>
              <div className="report-actions">
                <button type="button" onClick={() => void handleDecision(report.id, "ACCEPTED")}>
                  승인
                </button>
                <button
                  className="ghost-button"
                  type="button"
                  onClick={() => void handleDecision(report.id, "REJECTED")}
                >
                  반려
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
