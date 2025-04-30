import { add } from "../handler";

describe("handler", () => {
  describe("add", () => {
    test("adds two numbers together", () => {
      const result = add(1, 2);
      expect(result).toEqual(3);
    });
  });
});
