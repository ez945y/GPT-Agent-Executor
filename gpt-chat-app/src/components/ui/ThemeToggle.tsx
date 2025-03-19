'use client';

interface ThemeToggleProps {
  theme: string;
  toggleTheme: () => void;
}

export default function ThemeToggle({ theme, toggleTheme }: ThemeToggleProps) {
  return (
    <button
      onClick={toggleTheme}
      className="fixed top-4 right-4 w-10 h-10 rounded-full bg-secondary text-white flex items-center justify-center shadow-md hover:bg-primary transition-colors"
      aria-label="Toggle theme"
    >
      {theme === 'dark' ? (
        <i className="fas fa-sun"></i>
      ) : (
        <i className="fas fa-moon"></i>
      )}
    </button>
  );
}