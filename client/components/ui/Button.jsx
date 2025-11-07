import React from 'react';

// Common icons (Lucide or Feather) are often passed as props
const Button = ({ children, onClick, variant = 'primary', disabled = false, className = '' }) => {
  let styleClasses = '';

  switch (variant) {
    case 'primary':
      // The core Electric Gold button with subtle small size and glow on hover
      styleClasses = `
        bg-electric-gold text-luxury-black font-semibold 
        hover:bg-deep-gold transition-all duration-300 
        shadow-sm hover:shadow-gold-glow 
        tracking-wider
      `;
      break;
    case 'secondary':
      // Outline button for less aggressive actions
      styleClasses = `
        bg-transparent text-electric-gold border border-electric-gold 
        hover:bg-electric-gold hover:text-luxury-black transition-all duration-300
        shadow-sm hover:shadow-gold-glow
      `;
      break;
    default:
      styleClasses = '';
  }

  const baseClasses = `
    font-poppins text-sm md:text-base py-2 px-6 rounded-lg 
    inline-flex items-center justify-center 
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  return (
    <button
      className={`${baseClasses} ${styleClasses} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
