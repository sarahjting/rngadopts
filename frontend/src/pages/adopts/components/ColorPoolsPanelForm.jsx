import { useState, useContext, useEffect } from "react";
import axios from "axios";
import AppContext from "context";
import GeneralModal from "components/modals/GeneralModal";
import FormTextInput from "components/form/FormTextInput";
import FormTextarea from "components/form/FormTextarea";

export default function ColorPoolsPanelForm({adopt, show, onSubmitted, onClose, colorPool = null}) {
    const {pushToast} = useContext(AppContext);
    const [errors, setErrors] = useState({});
    const [form, setForm] = useState({});
    const [isPreviewMode, setIsPreviewMode] = useState(true);

    function submitted() {
        setForm({name: "", colors: ""});
        onSubmitted();
    };

    useEffect(() => {
        setErrors({});
        setForm({name: colorPool?.name ?? "", colors: colorPool?.colors ?? ""});
        setIsPreviewMode(!!colorPool);
    }, [colorPool])
    
    function submit() {
        const fn = colorPool?.id ? axios.put : axios.post;
        fn(`adopts/${adopt.id}/color-pools${colorPool ? "/" + colorPool.id : ""}`, form)
            .then(() => {
                pushToast('Color pools updated.', 'success');
                submitted();
            })
            .catch((err) => {
                if (err.response?.status === 400) {
                    setErrors(err.response.data);
                } else {
                    throw err;
                }
            });
    }

    function deleteColorPool()
    {
        axios.delete(`adopts/${adopt.id}/color-pools/${colorPool.id}`)
            .then(() => {
                pushToast('Color pool deleted.', 'success');
                submitted();
            })
            .catch((err) => {
                if (err.response?.status === 400) {
                    setErrors(err.response.data);
                } else {
                    throw err;
                }
            });
    }

    const colorsCount = form.colors ? form.colors.split('\n').length : 0;
    const palettesCount = colorsCount > 0 ? Math.max(0, Math.floor((form.colors.split('\n')[0].split(/[\s,]+/).length - 1)/3)) : 0;
    const palettePreview = form.colors && (
        <div className="overflow-auto relative rounded-lg mb-3 max-h-96">
            <table className="w-full text-sm text-left">
                <thead>
                    <tr>
                        <th className="py-3 text-xs">Color</th>
                        {[...Array(palettesCount).keys()].map(i => (
                            <th className="py-3 px-2 text-xs" key={i} >
                                Palette{i + 1}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {form.colors.split('\n').map((line, lineKey) => {
                        const lineData = line.split(/[\s,]+/);
                        return lineData.length > 0 && (
                            <tr key={lineKey}>
                                <td>
                                    {lineData[0]}
                                </td>
                                {[...Array(palettesCount).keys()].map(i => (
                                    <td key={i}>
                                        <div title="Base" style={{display: "inline-block", width: "20px", height: "15px", backgroundColor: lineData[1 + i * 3]}}></div>
                                        <div title="Shading" style={{display: "inline-block", width: "20px", height: "15px", backgroundColor: lineData[2 + i * 3]}}></div>
                                        <div title="Highlight" style={{display: "inline-block", width: "20px", height: "15px", backgroundColor: lineData[3 + i * 3]}}></div>
                                    </td>
                                ))}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    )

    return (
        <GeneralModal 
            show={show}
            title={colorPool ? 'Update color pool' : 'Create new color pool'}
            onClose={onClose} 
            footer={(
                <div className="flex w-full gap-3">
                    {colorPool && (<button className="text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={deleteColorPool}>Delete</button>)}
                    <button className="grow text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={submit}>{colorPool ? 'Update' : 'Create'}</button>
                </div>
            )}
        >
            <div>
                <div>
                    <FormTextInput 
                        name="name"
                        errors={errors}
                        label="Name"
                        value={form.name}
                        onChange={(e) => setForm({...form, name: e.target.value})}
                    ></FormTextInput>
                    {isPreviewMode && (<>
                            {palettePreview}
                            <div className="text-right">
                                <button class="bg-blue-500 text-white px-2 py-1 rounded-lg text-sm" onClick={() => setIsPreviewMode(false)}>
                                    Edit palettes
                                </button>
                            </div>
                        </>)}
                    {!isPreviewMode && (<>
                        <FormTextarea 
                            name="colors"
                            errors={errors}
                            label="Colors"
                            value={form.colors}
                            onChange={(e) => setForm({...form, colors: e.target.value})}
                            wrap="off"
                            rows="10"
                            style={{"white-space": "nowrap"}}
                        ></FormTextarea>
                        <div className="text-right mb-3">
                            <button class="bg-blue-500 text-white px-2 py-1 rounded-lg text-sm" onClick={() => setIsPreviewMode(true)}>
                                Preview
                            </button>
                        </div>
                        <ul class="list-disc ml-4 text-sm">
                            <li>
                                Every color pool / color wheel must have at least one color. 
                            </li>
                            <li>
                                Every color must have at least one palette. A multi-palette color can be used for multi-colored markings (eg. FR's butterfly, blend, etc). 
                            </li>
                            <li>
                                Each palette must have 3 hex codes. A base hex code, shading hex code, and highlight hex code. Provide the same hex three times over if you don't want shading/highlights.
                            </li>
                            <li>
                                Enter every color on a new line. The line should be formatted in the following order, with a space or comma each datum:
                                <ul class="list-disc ml-4">
                                    <li>Name of the color</li>
                                    <li>The first color palette's base hex code, prefixed with a #</li>
                                    <li>The first color palette's shading hex code, prefixed with a #</li>
                                    <li>The first color palette's highlight hex code, prefixed with a #</li>
                                    <li>The second color palette's base hex code, prefixed with a #</li>
                                    <li>The second color palette's shading hex code, prefixed with a #</li>
                                    <li>The second color palette's highlight hex code, prefixed with a #</li>
                                    <li>Repeat until you have all colors assigned</li>
                                </ul>
                            </li>
                        </ul>
                    </>)}
                </div>
            </div>
        </GeneralModal>
    );
}