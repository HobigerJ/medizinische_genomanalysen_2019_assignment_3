#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Johanna Hobiger'


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"  # TODO

    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    
        print("Annotating VCF file")
        
        ##
        ## Example loop
        ##
        
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
# 24 gefunden!
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')
        #print(annotation_result)
        jsonobject = json.loads(annotation_result)
        return jsonobject

        #for i in range(198,199):
            #print(jsonobject[i])
            #for monitor in jsonobject['query']:
            #   print(monitor)
        #for object in jsonobject:
         #   if 'cadd' in object:
          #      if 'genename' in object['cadd']['gene']:
           #         print(object['cadd']['gene']['genename'])
                #for cadd in object['cadd']:
                #    if 'gene' in cadd:
                #        for gene in cadd['gene']:
                #            print(gene['genename'])



                #print(cadd)
                #for gene in cadd['gene']:
                #    print(gene)    
        
        
    
    
    def get_list_of_genes(self, jsonobject):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        genenames = set()
        for object in jsonobject:
            if 'cadd' in object:
                if 'genename' in object['cadd']['gene']:
                    genenames.add(object['cadd']['gene']['genename'])
                    
        print("Genenames: ", genenames)
    
    
    def get_num_variants_modifier(self, jsonobject):
        '''
        Print the number of variants with putative_impact "MODIFIER" 
        :return:
        '''
        counter = 0
        for object in jsonobject:
            if 'snpeff' in object:
                #if 'putative_impact' in object['snpeff']['ann']:
                key, value = "putative_impact", "MODIFIER"
                if key in object['snpeff']['ann'] and value == object['snpeff']['ann']['putative_impact']:
                    counter += 1
        print("Number of variants with putative impact 'Modifier': ", counter)  
        
    
    def get_num_variants_with_mutationtaster_annotation(self, jsonobject):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''

        counter = 0
        for object in jsonobject:
            if 'dbnsfp' in object:
                if 'mutationtaster' in object['dbnsfp']: #['ann']:
                    counter += 1
        print("Number of variants with a 'mutationtaster' annotation: ", counter)
        
    
    def get_num_variants_non_synonymous(self, jsonobject):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''

        counter = 0
        for object in jsonobject:
            if 'cadd' in object:
                #if 'putative_impact' in object['snpeff']['ann']:
                key, value = "consequence", "NON_SYNONYMOUS"
                if key in object['cadd'] and value == object['cadd']['consequence']:
                    counter += 1
        print("Number of variants with consequence 'NON_SYNONYMOUS': ", counter)  
        
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("TODO")
            
    
    def print_summary(self):
        data_structure = self.annotate_vcf_file()
        #print(data_structure)
        #self.get_list_of_genes(data_structure) # 7 
        #self.get_num_variants_modifier(data_structure) # 4
        #self.get_num_variants_with_mutationtaster_annotation(data_structure) # 5
        self.get_num_variants_non_synonymous(data_structure)
        #print("Print all results here")
    
    
def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



