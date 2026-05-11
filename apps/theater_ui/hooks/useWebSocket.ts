import { useState, useEffect } from 'react';

export interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export function useWebSocket(url: string) {
  const [events, setEvents] = useState<TheaterEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [lastEvent, setLastEvent] = useState<TheaterEvent | null>(null);

  useEffect(() => {
    // In a real implementation, this would connect to the given URL
    // For the demo purposes and because we are mocking the interaction,
    // we can simulate the events.
    setConnected(true);
  }, [url]);

  return { events, connected, lastEvent };
}
