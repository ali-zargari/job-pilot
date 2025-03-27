import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-3 py-1 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "bg-primary-600 text-white hover:bg-primary-700",
        primary: "bg-primary-600 text-white hover:bg-primary-700",
        outline: "bg-transparent text-gray-600 border border-gray-300 hover:bg-gray-100",
        secondary: "bg-secondary-600 text-white hover:bg-secondary-700",
        destructive: "bg-danger-600 text-white hover:bg-danger-700",
        danger: "bg-danger-600 text-white hover:bg-danger-700",
        success: "bg-success-600 text-white hover:bg-success-700",
        warning: "bg-warning-600 text-white hover:bg-warning-700",
      },
      size: {
        default: "text-sm",
        sm: "text-xs px-2.5 py-0.5",
        lg: "text-base px-4 py-1.5",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, size, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size }), className)} {...props} />
  );
}

export { Badge, badgeVariants }; 