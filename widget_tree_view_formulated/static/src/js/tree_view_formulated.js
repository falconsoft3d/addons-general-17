/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { onWillUpdateProps, onMounted, useEffect, useRef } from "@odoo/owl";

export class FormulatedListRenderer extends ListRenderer {
    setup() {
        super.setup();
        this.formulatedTotals = {};
        this.rootRef = useRef("root");
        
        onWillUpdateProps((nextProps) => {
            this.computeFormulatedTotals(nextProps);
        });
        
        this.computeFormulatedTotals(this.props);
        
        // After mount, manually update footer cells with formulated values
        onMounted(() => {
            console.log('🎬 onMounted ejecutado, actualizando footer...');
            this.updateFooterCells();
        });
        
        // Update footer whenever formulatedTotals change
        useEffect(() => {
            console.log('🔄 useEffect ejecutado, actualizando footer...');
            this.updateFooterCells();
        });
    }

    /**
     * Manually update footer cells with formulated values using DOM manipulation
     */
    updateFooterCells() {
        console.log('🔨 updateFooterCells llamado');
        // Use setTimeout to ensure DOM is fully rendered with Odoo's default values
        setTimeout(() => {
            console.log('⏱️ setTimeout ejecutado, buscando footer...');
            if (!this.rootRef.el) {
                console.warn('⚠️ this.rootRef.el no existe');
                return;
            }
            
            const footer = this.rootRef.el.querySelector('tfoot');
            if (!footer) {
                console.warn('⚠️ No se encontró tfoot');
                return;
            }
            
            console.log('✅ Footer encontrado');
            
            const columns = this.props.archInfo.columns;
            const footerCells = footer.querySelectorAll('td');
            
            console.log(`📊 Columnas totales: ${columns.length}, Celdas footer: ${footerCells.length}`);
            console.log(`🔍 Totales calculados:`, this.formulatedTotals);
            
            // Map cells to columns using data-name attribute or class
            for (const column of columns) {
                if (!column.options?.formulated || this.formulatedTotals[column.name] === undefined) {
                    continue;
                }
                
                console.log(`🎯 Procesando columna formulada: ${column.name}`);
                
                const value = this.formulatedTotals[column.name];
                
                // Find the cell for this column by matching the column name
                // Try multiple methods to find the correct cell
                let cell = null;
                
                // Method 1: Find by data-name attribute
                cell = footer.querySelector(`td[data-name="${column.name}"]`);
                console.log(`   Método 1 (data-name): ${cell ? 'encontrado' : 'no encontrado'}`);
                
                // Method 2: Find by matching position with visible columns
                if (!cell) {
                    console.log(`   🔍 Intentando Método 2 (posición visible)...`);
                    const visibleColumns = columns.filter(c => !c.invisible && c.name);
                    console.log(`   📋 Columnas visibles: ${visibleColumns.length}`, visibleColumns.map(c => c.name));
                    const columnIndex = visibleColumns.indexOf(column);
                    console.log(`   📍 Índice de columna "${column.name}": ${columnIndex}`);
                    if (columnIndex >= 0) {
                        const visibleCells = Array.from(footerCells).filter(c => 
                            !c.classList.contains('o_list_record_selector')
                        );
                        console.log(`   📊 Celdas visibles en footer: ${visibleCells.length}`);
                        cell = visibleCells[columnIndex];
                        console.log(`   Método 2: ${cell ? 'encontrado ✅' : 'no encontrado ❌'}`);
                    }
                }
                
                if (!cell) {
                    console.warn(`   ⚠️ No se pudo encontrar celda para columna "${column.name}"`);
                    continue;
                }
                
                // Format value - always apply number formatting for numeric values
                let formattedValue;
                if (typeof value === 'number') {
                    const digits = column.digits ? column.digits[1] : 2;
                    // Manual formatting for Spanish locale (7.198,00)
                    const fixedValue = value.toFixed(digits);
                    const [intPart, decPart] = fixedValue.split('.');
                    const intFormatted = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                    formattedValue = `${intFormatted},${decPart}`;
                } else {
                    formattedValue = value.toString();
                }
                
                // Find and replace the content in the cell (may be inside a span)
                const spans = cell.querySelectorAll('span');
                console.log(`   🎨 Actualizando celda con valor: ${formattedValue}`);
                if (spans.length > 0) {
                    console.log(`   📝 Actualizando span (${spans.length} spans encontrados)`);
                    const targetSpan = spans[spans.length - 1];
                    targetSpan.textContent = formattedValue;
                    targetSpan.classList.add('o_formulated_total');
                    console.log(`   ✅ Valor actualizado en span`);
                } else {
                    console.log(`   📝 Actualizando celda directamente (sin spans)`);
                    cell.innerHTML = `<span class="o_formulated_total">${formattedValue}</span>`;
                    console.log(`   ✅ Valor actualizado en celda`);
                }
            }
        }, 100); // Wait 100ms for Odoo to finish rendering
    }

    /**
     * Compute formulated totals for columns with formulated attribute
     */
    computeFormulatedTotals(props) {
        const columns = props.archInfo.columns;
        const records = props.list.records;
        
        console.log('🔧 Widget tree_formulated cargado, procesando columnas...');
        
        if (!records || records.length === 0) {
            console.log('⚠️ No hay registros para calcular');
            return;
        }
        
        for (const column of columns) {
            if (column.options && column.options.formulated) {
                console.log(`📊 Encontrada columna formulada: ${column.name}, fórmula: ${column.options.formulated}`);
                try {
                    const total = this.evaluateFormula(
                        column.options.formulated,
                        column.name,
                        records,
                        columns
                    );
                    this.formulatedTotals[column.name] = total;
                    console.log(`✅ Resultado calculado para ${column.name}: ${total}`);
                } catch (error) {
                    console.error(`❌ Error evaluando fórmula para ${column.name}:`, error);
                    this.formulatedTotals[column.name] = 'Error';
                }
            }
        }
    }

    /**
     * Evaluate a formula with the context of current records
     * @param {string} formula - The formula to evaluate (e.g., "valor1 + valor2")
     * @param {string} currentField - The current field name
     * @param {Array} records - The list records
     * @param {Array} columns - The column definitions
     * @returns {number} - The computed value
     */
    evaluateFormula(formula, currentField, records, columns) {
        
        // Build context with all field values from all records
        const context = {};
        
        // Get all unique field names from the formula and from records
        const fieldNames = this.extractFieldNames(formula);
        
        // Sum all values for each field (default behavior)
        for (const fieldName of fieldNames) {
            context[fieldName] = 0;
            for (const record of records) {
                const value = record.data[fieldName];
                if (typeof value === 'number') {
                    context[fieldName] += value;
                }
            }
        }
        
        // Also add current record totals if they have aggregates
        for (const column of columns) {
            if (column.name && !context.hasOwnProperty(column.name)) {
                context[column.name] = 0;
                for (const record of records) {
                    const value = record.data[column.name];
                    if (typeof value === 'number') {
                        context[column.name] += value;
                    }
                }
            }
        }
        
        // Add special aggregate functions: MAX, MIN, AVG, COUNT
        const aggregateFunctions = {
            MAX: (fieldName) => {
                const values = records
                    .map(r => r.data[fieldName])
                    .filter(v => typeof v === 'number');
                return values.length > 0 ? Math.max(...values) : 0;
            },
            MIN: (fieldName) => {
                const values = records
                    .map(r => r.data[fieldName])
                    .filter(v => typeof v === 'number');
                return values.length > 0 ? Math.min(...values) : 0;
            },
            AVG: (fieldName) => {
                const values = records
                    .map(r => r.data[fieldName])
                    .filter(v => typeof v === 'number');
                return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
            },
            COUNT: (fieldName) => {
                return records.filter(r => r.data[fieldName] !== undefined && r.data[fieldName] !== null).length;
            },
            SUM: (fieldName) => {
                return records
                    .map(r => r.data[fieldName])
                    .filter(v => typeof v === 'number')
                    .reduce((a, b) => a + b, 0);
            }
        };
        
        // Evaluate the formula in the context
        try {
            // Create a function that evaluates the formula with the context and aggregate functions
            const evaluator = new Function(
                ...Object.keys(context), 
                'MAX', 'MIN', 'AVG', 'COUNT', 'SUM', 'Math',
                `return ${formula};`
            );
            return evaluator(
                ...Object.values(context), 
                aggregateFunctions.MAX,
                aggregateFunctions.MIN,
                aggregateFunctions.AVG,
                aggregateFunctions.COUNT,
                aggregateFunctions.SUM,
                Math
            );
        } catch (error) {
            console.error('Formula evaluation error:', error);
            throw error;
        }
    }

    /**
     * Extract field names from a formula string
     * @param {string} formula - The formula string
     * @returns {Array} - Array of field names
     */
    extractFieldNames(formula) {
        // Match variable names (alphanumeric and underscore)
        const matches = formula.match(/[a-zA-Z_][a-zA-Z0-9_]*/g);
        return matches ? [...new Set(matches)] : [];
    }

    /**
     * Format float values
     */
    formatFloat(value, column) {
        const digits = column.digits ? column.digits[1] : 2;
        return value.toFixed(digits);
    }
}

export const formulatedListView = {
    ...listView,
    Renderer: FormulatedListRenderer,
};

registry.category("views").add("tree_formulated", formulatedListView);
