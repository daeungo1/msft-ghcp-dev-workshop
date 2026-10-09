import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { MemberSelect } from "./MemberSelect";

describe("MemberSelect", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("creates a member and forwards it to the parent", async () => {
    const onCreated = vi.fn();
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 2, name: "bob", role: "MEMBER" }), {
        status: 201,
        headers: { "Content-Type": "application/json" },
      }),
    );

    render(
      <MemberSelect
        members={[{ id: 1, name: "alice", role: "MEMBER" }]}
        selectedMemberId={1}
        onSelect={vi.fn()}
        onCreated={onCreated}
      />,
    );

    fireEvent.change(screen.getByLabelText("새 회원 이름"), {
      target: { value: "bob" },
    });
    fireEvent.click(screen.getByRole("button", { name: "가입" }));

    await waitFor(() =>
      expect(onCreated).toHaveBeenCalledWith({ id: 2, name: "bob", role: "MEMBER" }),
    );
  });
});
