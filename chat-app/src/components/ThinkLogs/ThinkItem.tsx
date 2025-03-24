'use client';
import { format, toZonedTime } from 'date-fns-tz';
import type { LogEntry } from '@/types';

interface ThinkItemProps {
  log: LogEntry;
}

export default function ThinkItem({ log }: ThinkItemProps) {

  const date = new Date(log.timestamp);
  const zonedTime = toZonedTime(date, 'Asia/Taipei');
  const formattedTime = format(zonedTime, 'HH:mm:ss');


  return (
  <div className="mb-3 p-4 rounded-lg shadow-md bg-white border border-gray-200">
    <div className="text-sm font-medium text-gray-800">{log.message}</div>
    <div className="text-xs text-gray-600 mt-2">
      {formattedTime}
    </div>
  </div>
  );
}
