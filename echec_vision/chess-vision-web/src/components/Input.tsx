import React from "react"

interface Props {
    placeholder?: string,
    text: string,
    setText: (text: string) => void
}


const Input = (props: Props) => {
    const {
        placeholder,
        text,
        setText
    } = props

    const handleChange = React.useCallback((event: any) => {
        setText(event.target.value)
    }, [setText])

    return (
        <div className="mb-3 pt-0">
            <input onChange={handleChange} value={text} type="text" placeholder={placeholder} className="px-3 py-4 placeholder-slate-300 text-slate-600 relative bg-white bg-white rounded text-base border border-slate-300 outline-none focus:outline-none focus:ring w-full" />
        </div>
    )
}

export default Input;