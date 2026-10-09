import { render, screen, waitFor } from "@testing-library/react";

import App from "./App";

function mockAppFetch(role: "MEMBER" | "ADMIN") {
  vi.stubGlobal(
    "fetch",
    vi.fn((input: string | URL) => {
      const url = String(input);
      if (url === "/api/members") {
        return Promise.resolve(
          new Response(
            JSON.stringify([{ id: 1, name: "alice", role }]),
            { status: 200, headers: { "Content-Type": "application/json" } },
          ),
        );
      }
      if (url === "/api/members/1/following") {
        return Promise.resolve(
          new Response(JSON.stringify([]), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }
      if (url === "/api/feed?limit=20") {
        return Promise.resolve(
          new Response(JSON.stringify({ items: [], next_before: null }), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }
      throw new Error(`Unexpected request: ${url}`);
    }),
  );
}

describe("App", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the report management tab only for admins", async () => {
    mockAppFetch("MEMBER");
    const { unmount } = render(<App />);

    await waitFor(() => expect(screen.getByRole("button", { name: "피드" })).toBeInTheDocument());
    expect(screen.queryByRole("button", { name: "신고 관리" })).not.toBeInTheDocument();

    unmount();
    vi.unstubAllGlobals();

    mockAppFetch("ADMIN");
    render(<App />);

    await waitFor(() => expect(screen.getByRole("button", { name: "신고 관리" })).toBeInTheDocument());
  });
});
