import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { setCurrentMemberId } from "../api";
import { Feed } from "./Feed";

function makePost(id: number, content: string) {
  return {
    id,
    author_id: 1,
    content,
    created_at: "2026-10-09T12:00:00+00:00",
  };
}

describe("Feed", () => {
  beforeEach(() => {
    setCurrentMemberId(1);
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("loads the next page with the cursor", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            items: Array.from({ length: 20 }, (_, index) => makePost(30 - index, `post ${index}`)),
            next_before: 11,
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            items: Array.from({ length: 5 }, (_, index) => makePost(10 - index, `more ${index}`)),
            next_before: null,
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      );

    render(
      <Feed
        authorNames={{ 1: "alice" }}
        currentMemberId={1}
        followingIds={[]}
        onFollowChange={vi.fn()}
        onError={vi.fn()}
      />,
    );

    await waitFor(() => expect(screen.getByText("post 0")).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: "더 보기" }));

    await waitFor(() => expect(screen.getByText("more 0")).toBeInTheDocument());
    expect(vi.mocked(fetch).mock.calls[1]?.[0]).toBe("/api/feed?limit=20&before=11");
  });
});
