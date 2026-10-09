import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { setCurrentMemberId } from "../api";
import { PostComposer } from "./PostComposer";

describe("PostComposer", () => {
  beforeEach(() => {
    setCurrentMemberId(1);
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the counter and submits a post", async () => {
    const onCreated = vi.fn();
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          id: 1,
          author_id: 1,
          content: "안녕하세요",
          created_at: "2026-10-09T12:00:00+00:00",
        }),
        { status: 201, headers: { "Content-Type": "application/json" } },
      ),
    );

    render(<PostComposer disabled={false} onCreated={onCreated} onError={vi.fn()} />);

    fireEvent.change(screen.getByLabelText("게시글 내용"), {
      target: { value: "안녕하세요" },
    });

    expect(screen.getByText("5 / 280")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "등록" }));

    await waitFor(() => expect(onCreated).toHaveBeenCalledTimes(1));
    expect(vi.mocked(fetch).mock.calls[0]?.[0]).toBe("/api/posts");
  });
});
