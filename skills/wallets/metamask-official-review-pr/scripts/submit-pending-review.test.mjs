import assert from "node:assert/strict";
import test from "node:test";

import { submitPendingReview } from "./submit-pending-review.mjs";

const HEAD_SHA = "a".repeat(40);
const PR_URL = "https://github.com/MetaMask/metamask-mobile/pull/123";

const pendingReview = (overrides = {}) => ({
  id: 456,
  state: "PENDING",
  body: "Review summary",
  commit_id: HEAD_SHA,
  html_url: `${PR_URL}#pullrequestreview-456`,
  user: { login: "reviewer" },
  ...overrides,
});

const createAdapters = ({
  headSha = HEAD_SHA,
  reviews = [pendingReview()],
  submittedState = "COMMENTED",
  postError,
} = {}) => {
  const calls = [];
  const executeGh = (args, input) => {
    calls.push({ args, input });
    if (args[0] === "pr") {
      return JSON.stringify({
        number: 123,
        url: PR_URL,
        headRefOid: headSha,
      });
    }
    if (args[1] === "user") {
      return JSON.stringify({ login: "reviewer" });
    }
    if (args.includes("--paginate")) {
      return JSON.stringify([reviews]);
    }
    if (postError) {
      throw new Error(postError);
    }
    return JSON.stringify({
      id: 456,
      state: submittedState,
      html_url: `${PR_URL}#pullrequestreview-456`,
    });
  };
  return { calls, executeGh };
};

test("submitPendingReview resends the stored summary with the requested event", () => {
  const adapters = createAdapters();
  const result = submitPendingReview(PR_URL, "COMMENT", adapters);
  const post = adapters.calls.at(-1);

  assert.equal(post.args[1], "repos/MetaMask/metamask-mobile/pulls/123/reviews/456/events");
  assert.equal(post.args.includes("POST"), true);
  assert.deepEqual(JSON.parse(post.input), {
    body: "Review summary",
    event: "COMMENT",
  });
  assert.deepEqual(result, {
    pullRequest: PR_URL,
    reviewId: 456,
    state: "COMMENTED",
    url: `${PR_URL}#pullrequestreview-456`,
    event: "COMMENT",
  });
});

test("submitPendingReview accepts Approve and Request changes", () => {
  const approve = createAdapters({ submittedState: "APPROVED" });
  assert.equal(submitPendingReview(PR_URL, "APPROVE", approve).event, "APPROVE");
  assert.equal(JSON.parse(approve.calls.at(-1).input).event, "APPROVE");

  const requestChanges = createAdapters({ submittedState: "CHANGES_REQUESTED" });
  assert.equal(
    submitPendingReview(PR_URL, "REQUEST_CHANGES", requestChanges).event,
    "REQUEST_CHANGES",
  );
});

test("submitPendingReview stops when the reviewer has no single pending review", () => {
  const none = createAdapters({ reviews: [] });
  assert.throws(() => submitPendingReview(PR_URL, "COMMENT", none), /has 0 pending reviews/u);
  assert.equal(none.calls.length, 3);

  const someoneElse = createAdapters({
    reviews: [pendingReview({ user: { login: "other" } })],
  });
  assert.throws(
    () => submitPendingReview(PR_URL, "COMMENT", someoneElse),
    /has 0 pending reviews/u,
  );
});

test("submitPendingReview stops when the stored summary is empty", () => {
  const adapters = createAdapters({ reviews: [pendingReview({ body: "  " })] });

  assert.throws(() => submitPendingReview(PR_URL, "COMMENT", adapters), /has no summary body/u);
  assert.equal(adapters.calls.length, 3);
});

test("submitPendingReview stops when the frozen head moved", () => {
  const adapters = createAdapters({ headSha: "b".repeat(40) });

  assert.throws(
    () => submitPendingReview(PR_URL, "COMMENT", adapters),
    /pull request head moved/u,
  );
  assert.equal(adapters.calls.length, 3);
});

test("submitPendingReview rejects an unknown event before calling gh", () => {
  const adapters = createAdapters();

  assert.throws(
    () => submitPendingReview(PR_URL, "LGTM", adapters),
    /event must be COMMENT, APPROVE, or REQUEST_CHANGES/u,
  );
  assert.equal(adapters.calls.length, 0);
});

test("submitPendingReview propagates the API write failure", () => {
  const adapters = createAdapters({ postError: "API denied the review" });

  assert.throws(
    () => submitPendingReview(PR_URL, "COMMENT", adapters),
    /API denied the review/u,
  );
});
