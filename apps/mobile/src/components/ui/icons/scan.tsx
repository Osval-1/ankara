import Svg, { Path, Rect } from 'react-native-svg';

export function Scan({ color = '#000', ...props }: React.ComponentProps<typeof Svg>) {
  return (
    <Svg width={24} height={24} viewBox="0 0 24 24" fill="none" {...props}>
      <Path d="M3 7V5a2 2 0 0 1 2-2h2" stroke={color} strokeWidth={2} strokeLinecap="round" />
      <Path d="M17 3h2a2 2 0 0 1 2 2v2" stroke={color} strokeWidth={2} strokeLinecap="round" />
      <Path d="M21 17v2a2 2 0 0 1-2 2h-2" stroke={color} strokeWidth={2} strokeLinecap="round" />
      <Path d="M7 21H5a2 2 0 0 1-2-2v-2" stroke={color} strokeWidth={2} strokeLinecap="round" />
      <Rect x={7} y={7} width={10} height={10} rx={1} stroke={color} strokeWidth={2} />
    </Svg>
  );
}
