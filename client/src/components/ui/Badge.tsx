import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'bg-primary-100 text-primary-800',
        secondary: 'bg-secondary-100 text-secondary-800',
        success: 'bg-success-100 text-success-800',
        danger: 'bg-danger-100 text-danger-800',
        warning: 'bg-warning-100 text-warning-800',
        info: 'bg-blue-100 text-blue-800',
        outline: 'text-gray-900 border border-gray-200',
        critical: 'bg-danger-500 text-white font-semibold',
        minor: 'bg-gray-100 text-gray-800',
        medium: 'bg-warning-100 text-warning-800',
      },
      size: {
        default: 'h-6',
        sm: 'h-5 text-[10px]',
        lg: 'h-7 text-sm',
      },
      withDot: {
        true: 'pl-1.5',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      withDot: false,
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  dotColor?: string;
}

function Badge({
  className,
  variant,
  size,
  withDot,
  dotColor,
  ...props
}: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size, withDot, className }))}>
      {withDot && (
        <div
          className={cn('mr-1 h-2 w-2 rounded-full', dotColor ? dotColor : 'bg-current')}
        />
      )}
      {props.children}
    </div>
  );
}

export { Badge, badgeVariants }; 