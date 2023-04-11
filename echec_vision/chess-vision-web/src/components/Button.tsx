import React from "react";
import classNames from 'classnames'

interface Props {
    onClick: () => void,
    type: 'second' | 'danger' | 'success',
    text?: string,
    icon?: JSX.Element,
    className?: string
}

const Button = (props: Props) => {
    const {
        onClick,
        text,
        icon,
        type,
        className
    } = props;

    const isIconButton = React.useMemo(() => !!icon, [icon]);

    const buttonClasses = React.useMemo(() => {
        switch(type) {
            case 'second':
                return "text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
            case 'danger':
                return "focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
            case 'success':
                return "focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-900"
            default:
                return ""
        }
            
    }, [type])

    const iconClasses = React.useMemo(() => {
        if (isIconButton) {
            return "flex justify-center items-center"
        }
        return ""
    }, [isIconButton])

    return (
        <button onClick={onClick} type="button" className={classNames(className, buttonClasses, iconClasses)}>
            { isIconButton && icon }
            { !isIconButton && text }
        </button>
    )
}

export default Button;