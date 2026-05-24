import type { CSSProperties } from "react";

type StarStyle = CSSProperties & {
  "--star-size": string;
  "--star-delay": string;
  "--star-duration": string;
  "--star-dx": string;
  "--star-dy": string;
};

function seededValue(index: number, salt: number) {
  const value = Math.sin(index * 12.9898 + salt * 78.233) * 43758.5453;
  return value - Math.floor(value);
}

function starStyle(index: number): StarStyle {
  const x = seededValue(index, 1) * 100;
  const y = seededValue(index, 2) * 100;
  const size = 0.7 + seededValue(index, 3) * 1.8;
  const duration = 9 + seededValue(index, 4) * 12;
  const delay = seededValue(index, 5) * -duration;
  const dx = (seededValue(index, 6) - 0.5) * 130;
  const dy = (seededValue(index, 7) - 0.5) * 130;

  return {
    left: `${x}%`,
    top: `${y}%`,
    "--star-size": `${size}px`,
    "--star-delay": `${delay}s`,
    "--star-duration": `${duration}s`,
    "--star-dx": `${dx}px`,
    "--star-dy": `${dy}px`,
  };
}

export function CosmicBackground() {
  return (
    <div className="cosmic-background" aria-hidden="true">
      {Array.from({ length: 130 }, (_, index) => (
        <span key={index} className="cosmic-star" style={starStyle(index + 1)} />
      ))}
    </div>
  );
}
