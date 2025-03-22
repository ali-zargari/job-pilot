import * as React from 'react';
import * as ProgressPrimitive from '@radix-ui/react-progress';
import { cn } from '@/lib/utils';

const Progress = React.forwardRef<
  React.ElementRef<typeof ProgressPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root> & {
    variant?: 'default' | 'success' | 'warning' | 'danger';
    showValue?: boolean;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
    value: number;
    max?: number;
  }
>(
  (
    { className, value, variant = 'default', showValue = false, size = 'md', max = 100, ...props },
    ref
  ) => {
    const getVariantClass = () => {
      switch (variant) {
        case 'success':
          return 'bg-success-500';
        case 'warning':
          return 'bg-warning-500';
        case 'danger':
          return 'bg-danger-500';
        default:
          return 'bg-primary-500';
      }
    };

    const getSizeClass = () => {
      switch (size) {
        case 'sm':
          return 'h-2';
        case 'lg':
          return 'h-6';
        default:
          return 'h-4';
      }
    };

    return (
      <div className={cn('relative flex items-center gap-2', className)}>
        <ProgressPrimitive.Root
          ref={ref}
          className={cn(
            'relative overflow-hidden rounded-full bg-gray-200 w-full',
            getSizeClass()
          )}
          value={value}
          max={max}
          {...props}
        >
          <ProgressPrimitive.Indicator
            className={cn(
              'h-full transition-all',
              getVariantClass()
            )}
            style={{ transform: `translateX(-${100 - (value / max) * 100}%)` }}
          />
        </ProgressPrimitive.Root>
        {showValue && (
          <div className="min-w-[40px] text-sm font-medium">{Math.round(value)}%</div>
        )}
      </div>
    );
  }
);

Progress.displayName = ProgressPrimitive.Root.displayName;

export { Progress }; 