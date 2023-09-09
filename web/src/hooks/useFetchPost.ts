import { useCallback, useState } from "react";

interface UseFetchPostProps<T> {
  url: string;
  mockResponse?: (body: unknown) => Promise<T>;
}

interface FetchPostResponse<T = unknown> {
  isLoading: boolean;
  error: Error | null;
  data: T | null;
  triggerRequest: (body: unknown) => Promise<T>;
}

function useFetchPost<T = unknown>(
  props: UseFetchPostProps<T>,
): FetchPostResponse<T> {
  const [isLoading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [data, setData] = useState<T | null>(null);

  const triggerRequest = useCallback(
    async (body: unknown) => {
      setLoading(true);
      setError(null);

      try {
        if (props.mockResponse != null) {
          const responseData = await props.mockResponse(body);
          setData(responseData as T);
          setLoading(false);
          return;
        }

        const response = await fetch(props.url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        setData(responseData as T);

        return responseData;
      } catch (error) {
        setError(error as Error);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [props.url],
  );

  return { isLoading, error, data, triggerRequest };
}

export default useFetchPost;
