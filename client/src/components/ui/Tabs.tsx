import * as React from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import { cn } from '@/lib/utils';

const Tabs = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Root> & {
    variant?: 'default' | 'pills' | 'underline' | 'boxed';
  }
>(({ className, variant = 'default', ...props }, ref) => (
  <TabsPrimitive.Root
    ref={ref}
    className={cn('w-full', className)}
    {...props}
  />
));
Tabs.displayName = TabsPrimitive.Root.displayName;

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List> & {
    variant?: 'default' | 'pills' | 'underline' | 'boxed';
  }
>(({ className, variant = 'default', ...props }, ref) => {
  const variantClasses = {
    default: 'bg-gray-100 rounded-lg p-1',
    pills: 'space-x-1',
    underline: 'border-b border-gray-200',
    boxed: 'grid w-full grid-flow-col auto-cols-fr divide-x divide-gray-200 rounded-lg border border-gray-200 bg-white',
  };

  return (
    <TabsPrimitive.List
      ref={ref}
      className={cn(
        'flex h-10 items-center justify-center text-gray-500',
        variantClasses[variant as keyof typeof variantClasses],
        className
      )}
      {...props}
    />
  );
});
TabsList.displayName = TabsPrimitive.List.displayName;

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger> & {
    variant?: 'default' | 'pills' | 'underline' | 'boxed';
  }
>(({ className, variant = 'default', ...props }, ref) => {
  const variantClasses = {
    default: 'data-[state=active]:bg-white data-[state=active]:text-primary-600 data-[state=active]:shadow-sm',
    pills: 'data-[state=active]:bg-primary-600 data-[state=active]:text-white rounded-md',
    underline: 'border-b-2 border-transparent data-[state=active]:border-primary-600 data-[state=active]:text-primary-600',
    boxed: 'data-[state=active]:bg-gray-50 data-[state=active]:text-primary-600 h-full w-full',
  };

  return (
    <TabsPrimitive.Trigger
      ref={ref}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap px-3 py-1.5 text-sm font-medium ring-offset-white transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant as keyof typeof variantClasses],
        className
      )}
      {...props}
    />
  );
});
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName;

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      'mt-2 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2',
      className
    )}
    {...props}
  />
));
TabsContent.displayName = TabsPrimitive.Content.displayName;

export { Tabs, TabsList, TabsTrigger, TabsContent }; 