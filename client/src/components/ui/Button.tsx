import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary-500 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default: 'bg-primary-600 text-white hover:bg-primary-700 shadow-button',
        destructive: 'bg-danger-600 text-white hover:bg-danger-700 shadow-button',
        outline: 'border border-gray-300 bg-white hover:bg-gray-50 text-gray-700',
        secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 shadow-button',
        ghost: 'hover:bg-gray-100 text-gray-700 shadow-none',
        link: 'text-primary-600 underline-offset-4 hover:underline shadow-none',
        success: 'bg-success-600 text-white hover:bg-success-700 shadow-button',
        warning: 'bg-warning-600 text-white hover:bg-warning-700 shadow-button',
        premium: 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white hover:from-primary-700 hover:to-secondary-700 shadow-button',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-8 px-3 text-sm',
        lg: 'h-12 px-6 text-lg',
        xl: 'h-14 px-8 text-xl',
        icon: 'h-10 w-10',
      },
      fullWidth: {
        true: 'w-full',
      },
      withIcon: {
        true: 'gap-2',
      },
      animated: {
        true: 'transform hover:scale-105',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      fullWidth: false,
      withIcon: false,
      animated: false,
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, fullWidth, withIcon, animated, asChild = false, ...props }, ref) => {
    const Comp = asChild ? React.Fragment : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, fullWidth, withIcon, animated, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';

export { Button, buttonVariants }; 