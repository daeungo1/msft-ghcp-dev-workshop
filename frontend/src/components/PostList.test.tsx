import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { setCurrentMemberId } from "../api";
import { PostList } from "./PostList";

describe("PostList", () => {
  beforeEach(() => {
    setCurrentMemberId(1);
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("toggles follow state for another author", async () => {
    const onFollowChange = vi.fn();
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify([
            {
              id: 10,
              author_id: 2,
              content: "안녕하세요",
              created_at: "2026-10-09T12:00:00+00:00",
            },
          ]),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      .mockResolvedValueOnce(new Response(JSON.stringify({}), { status: 201 }));

    render(
      <PostList
        authorNames={{ 2: "bob" }}
        currentMemberId={1}
        followingIds={[]}
        onFollowChange={onFollowChange}
        onError={vi.fn()}
      />,
    );

    await waitFor(() => expect(screen.getByText("안녕하세요")).toBeInTheDocument());

    fireEvent.click(screen.getByRole("button", { name: "팔로우" }));

    await waitFor(() => expect(onFollowChange).toHaveBeenCalledWith(2, true));
  });
});
