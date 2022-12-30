import { useState } from "react";
import ColorPoolFormModal from "pages/adopts/components/modals/ColorPoolFormModal";

export default function ColorPoolsPanel({adopt, colorPools, onSubmitted = (() => {})}) {
    const [showModal, setShowModal] = useState(false);
    const [currentColorPool, setCurrentColorPool] = useState(null);

    function submitted() {
        setShowModal(false);
        onSubmitted();
    }

    function pushCreateModal() {
        setCurrentColorPool(null);
        setShowModal(true);
    }

    function pushUpdateModal(adoptLayer) {
        setCurrentColorPool(adoptLayer);
        setShowModal(true);
    }

    return colorPools ? (
        <div>
            {colorPools.length ? (
            <div className="overflow-x-auto relative rounded-lg mb-3">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 border-b border-gray-50">
                        <tr>
                            <th className="py-3 px-6">Color pool</th>
                            <th className="py-3 px-6">Colors</th>
                            <th className="py-3 px-6">Palettes</th>
                        </tr>
                    </thead>
                    <tbody className="bg-gray-50 border-b">
                    {colorPools.map((colorPool, key) => (
                        <tr key={key} className="border-b border-gray-100">
                            <td className="py-4 px-6">
                                <button className="text-blue-500" onClick={() => pushUpdateModal(colorPool)}>
                                    {colorPool.name}
                                </button>
                            </td>
                            <td className="py-4 px-6">
                                {colorPool.colors_count}
                            </td>
                            <td className="py-4 px-6">
                                {colorPool.palettes_count}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            ) : (<div className="mb-3">No color pools have been added to this adopt yet.</div>)}
            <button className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full" onClick={pushCreateModal}>
                Add new color pool
            </button>
            <ColorPoolFormModal 
                adopt={adopt} 
                colorPool={currentColorPool} 
                show={showModal} 
                onSubmitted={submitted} 
                onClose={() => 
                setShowModal(false)}
            ></ColorPoolFormModal>
        </div>
    ) : (<>Loading...</>);
}