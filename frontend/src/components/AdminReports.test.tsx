import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { setCurrentMemberId } from "../api";
import { AdminReports } from "./AdminReports";

describe("AdminReports", () => {
  beforeEach(() => {
    setCurrentMemberId(1);
    vi.stubGlobal(
      "fetch",
      vi.fn((input: string | URL, init?: RequestInit) => {
        const url = String(input);
        if (url === "/api/reports?status=OPEN" && !init?.method) {
          return Promise.resolve(
            new Response(
              JSON.stringify([
                {
                  id: 1,
                  post_id: 7,
                  reporter_id: 2,
                  reason: "spam content",
                  status: "OPEN",
                  created_at: "2026-10-09T12:00:00+00:00",
                },
                {
                  id: 2,
                  post_id: 8,
                  reporter_id: 3,
                  reason: "bad words",
                  status: "OPEN",
                  created_at: "2026-10-09T12:05:00+00:00",
                },
              ]),
              { status: 200, headers: { "Content-Type": "application/json" } },
            ),
          );
        }
        if (url === "/api/reports/1" && init?.method === "PATCH") {
          return Promise.resolve(
            new Response(
              JSON.stringify({
                id: 1,
                post_id: 7,
                reporter_id: 2,
                reason: "spam content",
                status: "ACCEPTED",
                created_at: "2026-10-09T12:00:00+00:00",
              }),
              { status: 200, headers: { "Content-Type": "application/json" } },
            ),
          );
        }
        if (url === "/api/reports/2" && init?.method === "PATCH") {
          return Promise.resolve(
            new Response(
              JSON.stringify({
                id: 2,
                post_id: 8,
                reporter_id: 3,
                reason: "bad words",
                status: "REJECTED",
                created_at: "2026-10-09T12:05:00+00:00",
              }),
              { status: 200, headers: { "Content-Type": "application/json" } },
            ),
          );
        }
        throw new Error(`Unexpected request: ${url}`);
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("sends accept and reject decisions", async () => {
    render(<AdminReports onError={vi.fn()} />);

    await waitFor(() => expect(screen.getByText("spam content")).toBeInTheDocument());

    fireEvent.click(within(screen.getByText("spam content").closest("li")!).getByRole("button", { name: "승인" }));
    await waitFor(() => expect(screen.queryByText("spam content")).not.toBeInTheDocument());

    fireEvent.click(within(screen.getByText("bad words").closest("li")!).getByRole("button", { name: "반려" }));
    await waitFor(() => expect(screen.queryByText("bad words")).not.toBeInTheDocument());

    expect(vi.mocked(fetch).mock.calls.some(([url]) => url === "/api/reports/1")).toBe(true);
    expect(vi.mocked(fetch).mock.calls.some(([url]) => url === "/api/reports/2")).toBe(true);
  });
});
